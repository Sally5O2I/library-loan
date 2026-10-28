"""샘플 테스트 5개로 solution.py를 확인합니다.  실행: python check.py   (이 파일은 수정하지 마세요)"""
import contextlib, importlib.util, io, os, traceback

HERE = os.path.dirname(os.path.abspath(__file__))

def _new(m):
    return m.LibraryLoan()

def _eq(got, want, what):
    assert got == want, f"{what} → {got!r}, 정답 {want!r}"

# --- 샘플 테스트 5개 ---
def test_01(m):
    "정상 대출 → True"
    lib = _new(m); _eq(lib.borrow("B001", "김철수", 1), True, "borrow B001")

def test_02(m):
    "이미 대출 중인 책 → False"
    lib = _new(m); lib.borrow("B001", "김철수", 1)
    _eq(lib.borrow("B001", "이영희", 2), False, "borrow B001 again")

def test_03(m):
    "기한 안에 반납 → 연체 0"
    lib = _new(m); lib.borrow("B001", "김철수", 1)
    _eq(lib.return_book("B001", "김철수", 10), 0, "return day 10")

def test_04(m):
    "대출 목록은 반납 기한 순"
    lib = _new(m); lib.borrow("B003", "김철수", 5); lib.borrow("B002", "김철수", 2)
    _eq(lib.get_loans("김철수"), [("B002", 16), ("B003", 19)], "get_loans")

def test_05(m):
    "남이 빌린 책 반납 → -1"
    lib = _new(m); lib.borrow("B001", "김철수", 1)
    _eq(lib.return_book("B001", "이영희", 3), -1, "return by 이영희")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    path = os.path.join(HERE, "solution.py")
    try:
        spec = importlib.util.spec_from_file_location("solution", path)
        sol = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(sol)
    except Exception:
        print("solution.py 를 불러오지 못했습니다. 아래 에러를 Claude에게 그대로 보여 주세요.\n")
        traceback.print_exc()
        raise SystemExit(1)

    print("샘플 테스트 5개 실행\n")
    passed = 0
    for t in TESTS:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                t(sol)
            passed += 1
            print(f"  [통과] {t.__doc__}")
        except AssertionError as e:
            print(f"  [실패] {t.__doc__}  ({e})")
        except Exception as e:
            print(f"  [에러] {t.__doc__}  ({type(e).__name__}: {e})")
    print(f"\n결과: {passed} / {len(TESTS)} 통과")
    if passed == len(TESTS):
        print("5개 모두 통과! 1단계 끝. 실제 점수(80점)는 블라인드 테스트 20개로 매깁니다. 문제지 4단계 확인표까지 꼭 해 보세요.")

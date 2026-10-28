"""블라인드 대비 추가 테스트.  실행: python my_test.py"""
from solution import LibraryLoan

TESTS = []


def test(f):
    TESTS.append(f)
    return f


@test
def problem_example():
    lib = LibraryLoan()
    assert lib.borrow("B001", "김철수", 1) is True
    assert lib.borrow("B001", "이영희", 2) is False
    assert lib.get_loans("김철수") == [("B001", 15)]
    assert lib.return_book("B001", "이영희", 5) == -1
    assert lib.return_book("B001", "김철수", 18) == 3
    assert lib.borrow("B002", "김철수", 19) is False
    assert lib.borrow("B002", "김철수", 21) is True


@test
def checklist_1_to_10():
    lib = LibraryLoan()
    assert lib.borrow("B001", "김민수", 1) is True                       # 1
    assert lib.borrow("B001", "박지은", 2) is False                      # 2
    assert lib.borrow("B002", "김민수", 2) is True                       # 3
    assert lib.borrow("B003", "김민수", 2) is True
    assert lib.borrow("B004", "김민수", 2) is False                      # 4
    assert lib.borrow("B009", "박지은", 2) is False                      # 5
    assert lib.return_book("B001", "김민수", 10) == 0                    # 6
    assert lib.get_loans("김민수") == [("B002", 16), ("B003", 16)]       # 7
    assert lib.borrow("B004", "김민수", 20) is False                     # 8
    assert lib.return_book("B002", "김민수", 20) == 4                    # 9
    assert lib.return_book("B003", "김민수", 20) == 4
    assert lib.borrow("B004", "김민수", 23) is False                     # 10
    assert lib.borrow("B004", "김민수", 24) is True


BAD_DAYS = [0, -1, 2.5, 2.0, "3", None, True, False]


@test
def bad_day_borrow():
    lib = LibraryLoan()
    for d in BAD_DAYS:
        assert lib.borrow("B001", "김철수", d) is False, d
        assert lib.get_loans("김철수") == []


@test
def bad_day_return():
    lib = LibraryLoan()
    assert lib.borrow("B001", "김철수", 1) is True
    for d in BAD_DAYS:
        assert lib.return_book("B001", "김철수", d) == -1, d
        assert lib.get_loans("김철수") == [("B001", 15)]


@test
def return_day_boundaries():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    assert lib.return_book("B001", "a", 15) == 0       # 기한 당일
    lib.borrow("B002", "b", 1)
    assert lib.return_book("B002", "b", 16) == 1       # 기한 +1
    lib.borrow("B003", "c", 5)
    assert lib.return_book("B003", "c", 5) == 0        # 빌린 날 당일
    lib.borrow("B004", "d", 5)
    assert lib.return_book("B004", "d", 4) == -1       # 빌린 날보다 이름
    assert lib.get_loans("d") == [("B004", 19)]


@test
def invalid_returns_and_ids():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    assert lib.return_book("B001", "a", 2) == 0
    assert lib.return_book("B001", "a", 3) == -1       # 이미 반납
    assert lib.return_book("B009", "a", 3) == -1       # 없는 책
    assert lib.return_book("B002", "a", 3) == -1       # 안 빌린 책
    assert lib.borrow("b001", "a", 3) is False         # 소문자
    assert lib.get_loans("a") == []


@test
def failures_do_not_change_state():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.borrow("B002", "a", 2)
    before = lib.get_loans("a")
    assert lib.borrow("B001", "b", 3) is False
    assert lib.borrow("B009", "a", 3) is False
    assert lib.return_book("B001", "b", 3) == -1
    assert lib.return_book("B001", "a", 0) == -1
    assert lib.get_loans("a") == before
    assert lib.get_loans("b") == []
    # 연체 중 대출 실패 뒤에도 정지가 생기지 않아야 함
    assert lib.borrow("B003", "a", 17) is False
    assert lib.return_book("B001", "a", 15) == 0
    assert lib.return_book("B002", "a", 16) == 0
    assert lib.borrow("B003", "a", 17) is True


@test
def three_book_limit_then_return():
    lib = LibraryLoan()
    for b in ("B001", "B002", "B003"):
        assert lib.borrow(b, "a", 1) is True
    assert lib.borrow("B004", "a", 1) is False
    assert lib.return_book("B002", "a", 2) == 0
    assert lib.borrow("B004", "a", 2) is True


@test
def overdue_holding_boundary():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)                         # 기한 15
    assert lib.borrow("B002", "a", 15) is True         # 기한 당일 OK
    lib2 = LibraryLoan()
    lib2.borrow("B001", "a", 1)
    assert lib2.borrow("B002", "a", 16) is False       # 기한+1 실패


@test
def suspension_boundary_overlap_and_isolation():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    assert lib.return_book("B001", "a", 18) == 3       # 정지 18~20
    assert lib.borrow("B002", "a", 20) is False        # 마지막 날
    assert lib.borrow("B002", "a", 21) is True         # 다음 날
    assert lib.borrow("B003", "b", 19) is True         # 다른 사람 영향 없음

    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.borrow("B002", "a", 1)
    assert lib.return_book("B001", "a", 25) == 10      # 정지 25~34
    assert lib.return_book("B002", "a", 26) == 11      # 정지 26~36 → 36까지
    assert lib.borrow("B003", "a", 36) is False
    assert lib.borrow("B003", "a", 37) is True         # 합산(46)이 아님


@test
def shorter_later_suspension_keeps_longer():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.borrow("B002", "a", 10)                        # 기한 24
    assert lib.return_book("B001", "a", 25) == 10      # 정지 25~34
    assert lib.return_book("B002", "a", 26) == 2       # 정지 26~27, 34 유지
    assert lib.borrow("B003", "a", 34) is False
    assert lib.borrow("B003", "a", 35) is True


@test
def returned_book_borrowable_and_sort():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.return_book("B001", "a", 2)
    assert lib.borrow("B001", "b", 3) is True
    lib2 = LibraryLoan()
    lib2.borrow("B003", "c", 1)
    lib2.borrow("B001", "c", 1)
    lib2.borrow("B002", "c", 1)
    assert lib2.get_loans("c") == [("B001", 15), ("B002", 15), ("B003", 15)]
    assert lib2.get_loans("모르는사람") == []


@test
def return_allowed_while_suspended():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.borrow("B002", "a", 1)
    assert lib.return_book("B001", "a", 20) == 5       # 정지 20~24
    assert lib.return_book("B002", "a", 21) == 6       # 정지 중에도 반납 OK


@test
def borrow_date_order_not_checked():
    lib = LibraryLoan()
    assert lib.borrow("B001", "a", 5) is True
    assert lib.borrow("B002", "a", 2) is True          # 5일째 다음 2일째도 성공
    assert lib.get_loans("a") == [("B002", 16), ("B001", 19)]
    assert lib.return_book("B001", "a", 4) == -1       # 빌린 날보다 이른 반납은 실패


@test
def suspension_only_blocks_its_window():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 10)                        # 기한 24
    assert lib.return_book("B001", "a", 30) == 6       # 정지 30~35
    assert lib.borrow("B002", "a", 29) is True         # 정지 시작 전 날짜는 성공
    lib2 = LibraryLoan()
    lib2.borrow("B001", "a", 10)
    lib2.return_book("B001", "a", 30)
    assert lib2.borrow("B002", "a", 30) is False       # 정지 첫날
    assert lib2.borrow("B002", "a", 35) is False       # 정지 마지막 날
    assert lib2.borrow("B002", "a", 36) is True


@test
def overlapping_suspension_out_of_order_returns():
    lib = LibraryLoan()
    lib.borrow("B001", "a", 1)
    lib.borrow("B002", "a", 1)
    assert lib.return_book("B001", "a", 26) == 11      # 정지 26~36 (먼저 기록)
    assert lib.return_book("B002", "a", 25) == 10      # 정지 25~34 (날짜는 더 이름)
    assert lib.borrow("B003", "a", 36) is False
    assert lib.borrow("B003", "a", 37) is True


if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            passed += 1
            print(f"  [통과] {t.__name__}")
        except AssertionError as e:
            print(f"  [실패] {t.__name__}  {e!r}")
    print(f"\n결과: {passed} / {len(TESTS)} 통과")

# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # bool은 int의 하위 타입이므로 type(...) is int 로 걸러낸다
    return type(day) is int and day >= 1


class LibraryLoan:
    def __init__(self):
        self.loans = {}           # book_id -> (name, 빌린 날)
        self.suspensions = {}     # name -> [(정지 시작일, 정지 마지막 날), ...]

    def _books_of(self, name):
        return [(book_id, borrowed + LOAN_DAYS)
                for book_id, (who, borrowed) in self.loans.items() if who == name]

    def borrow_fail_reason(self, book_id, name, day):
        """대출이 실패하는 이유를 돌려준다. 대출할 수 있으면 None. (기록은 바꾸지 않음)"""
        if book_id not in BOOKS:
            return "없는 책 번호입니다."
        if not _valid_day(day):
            return "날짜는 1 이상의 정수로 입력해야 합니다."
        if book_id in self.loans:
            return "이미 대출된 도서입니다."
        mine = self._books_of(name)
        if len(mine) >= MAX_LOANS:
            return "이미 3권을 빌리고 있습니다."
        overdue = [f"{b}(기한 {due}일째)" for b, due in sorted(mine) if day > due]
        if overdue:
            return "반납 기한이 지난 책을 아직 갖고 있습니다: " + ", ".join(overdue)
        # 날짜 순서는 검사하지 않으므로, day가 정지 구간 안에 있을 때만 막는다
        for start, end in self.suspensions.get(name, []):
            if start <= day <= end:
                return f"현재 대출 정지 상태입니다. ({start}일째 ~ {end}일째)"
        return None

    def borrow(self, book_id, name, day):
        # 모든 검사를 먼저 끝내고, 통과했을 때만 기록을 바꾼다
        if self.borrow_fail_reason(book_id, name, day) is not None:
            return False
        self.loans[book_id] = (name, day)
        return True

    def return_fail_reason(self, book_id, name, day):
        """반납이 실패하는 이유를 돌려준다. 반납할 수 있으면 None. (기록은 바꾸지 않음)"""
        if not _valid_day(day):
            return "날짜는 1 이상의 정수로 입력해야 합니다."
        if book_id not in BOOKS:
            return "없는 책 번호입니다."
        if book_id not in self.loans:
            return "대출 중인 책이 아닙니다."
        who, borrowed = self.loans[book_id]
        if who != name:
            return "이 이름으로 빌린 책이 아닙니다."
        if day < borrowed:
            return f"빌린 날({borrowed}일째)보다 이른 날짜입니다."
        return None

    def return_book(self, book_id, name, day):
        if self.return_fail_reason(book_id, name, day) is not None:
            return -1
        _, borrowed = self.loans[book_id]
        overdue = max(0, day - (borrowed + LOAN_DAYS))
        del self.loans[book_id]
        if overdue > 0:
            # 정지 구간을 그대로 기록한다. 겹치면 구간이 합쳐져 더 늦게 끝나는 쪽까지 막힌다 (합산하지 않음)
            self.suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        return sorted(self._books_of(name), key=lambda loan: (loan[1], loan[0]))

    def get_all_loans(self):
        """지금 대출 중인 모든 책: (book_id, name, 빌린 날, 반납 기한) 목록, 반납 기한·책 번호 순"""
        rows = [(book_id, who, borrowed, borrowed + LOAN_DAYS)
                for book_id, (who, borrowed) in self.loans.items()]
        return sorted(rows, key=lambda row: (row[3], row[0]))

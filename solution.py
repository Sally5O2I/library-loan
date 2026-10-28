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

    def borrow(self, book_id, name, day):
        # 모든 검사를 먼저 끝내고, 통과했을 때만 기록을 바꾼다
        if book_id not in BOOKS:
            return False
        if not _valid_day(day):
            return False
        if book_id in self.loans:
            return False
        mine = self._books_of(name)
        if len(mine) >= MAX_LOANS:
            return False
        if any(day > due for _, due in mine):
            return False
        # 날짜 순서는 검사하지 않으므로, day가 정지 구간 안에 있을 때만 막는다
        if any(start <= day <= end for start, end in self.suspensions.get(name, [])):
            return False
        self.loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_day(day):
            return -1
        if book_id not in BOOKS or book_id not in self.loans:
            return -1
        who, borrowed = self.loans[book_id]
        if who != name:
            return -1
        if day < borrowed:
            return -1
        overdue = max(0, day - (borrowed + LOAN_DAYS))
        del self.loans[book_id]
        if overdue > 0:
            # 정지 구간을 그대로 기록한다. 겹치면 구간이 합쳐져 더 늦게 끝나는 쪽까지 막힌다 (합산하지 않음)
            self.suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        return sorted(self._books_of(name), key=lambda loan: (loan[1], loan[0]))

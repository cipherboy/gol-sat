import cmsh


class Board:
    model: cmsh.Model
    width: int
    height: int

    squares: list
    bvars: list

    def __init__(self, model: cmsh.Model, width: int, height: int):
        self.model = model
        self.width = width
        self.height = height

        self.squares = [
            [
                None
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

        self.bvars = [
            [
                self.model.var()
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

    def dead(self, x: int, y: int):
        self.squares[y][x] = True

    def alive(self, x: int, y: int):
        self.squares[y][x] = False

    def unmark(self, x: int, y: int):
        self.squares[y][x] = None

    def from_array(self, board: list):
        assert len(board) == self.height
        for y, col in enumerate(board):
            assert len(col) == self.width
            for x, square in enumerate(col):
                self.squares[y][x] = square

    def add_asserts(self):
        for y, col in enumerate(self.squares):
            for x, square in enumerate(col):
                if square is True:
                    self.model.add_assert(self.bvars[y][x] == True)
                elif square is False:
                    self.model.add_assert(self.bvars[y][x] == False)

    def as_vec(self) -> cmsh.Vector:
        vecs = []
        for col in self.bvars:
            v_col = self.model.to_vec(col)
            vecs.append(v_col)

        return self.model.join_vec(vecs)

    def __str__(self):
        result = "==== board " + str(self.width) + "x" + str(self.height) + " ====\n"
        if self.model.sat:
            for col in self.bvars:
                for square in col:
                    if bool(square):
                        result += "x"
                    else:
                        result += "_"
                result += "\n"
        else:
            for col in self.squares:
                for square in col:
                    if square is True:
                        result += "x"
                    elif square is False:
                        result += "_"
                    elif square is None:
                        result += "?"
                result += "\n"

        return result.strip()

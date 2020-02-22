from collections import deque

# files
infiles = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']
outfiles = ['a_example.out', 'b_read_on.out', 'c_incunabula.out','d_tough_choices.out', 'e_so_many_books.out', 'f_libraries_of_the_world.out']

class Library:
    def __init__(self):
        self.id = 0
        self.index = 0
        self.num_books = 0
        self.signup_time = 0
        self.scans_per_day = 0
        self.score = 0
        self.books = []
        self.current_book = 0
        self.total_scanned_books = 0
        self.scanned_books = []
        self.average = 0

class Problem:
    def __init__(self):
        self.B = 0
        self.L = 0
        self.D = 0
        self.bookScores = []
        self.libraries = []
        self.currLib = 0
        self.scanned_books = set()
        self.result_libraries = []
        self.infile = ''

    def read_file(self, infile):
        self.infile = infile
        with open(infile, 'r') as reader:
            for i, line in enumerate(reader):
                line = [int(x) for x in line.split()]
                if len(line) == 0:
                    continue
                # B - Books, L - Libraries, D - days
                if i == 0:
                    self.B, self.L, self.D = line[0], line[1], line[2]
                # Scores of each books
                elif i == 1:
                    self.bookScores = line
                # books in library, time in days to signup, number of books scanned each day
                elif i >= 2 and i % 2 == 0:
                    library = Library()
                    library.id = self.currLib
                    library.num_books = line[0]
                    library.signup_time = line[1]
                    library._signup_time = line[1]
                    library.scans_per_day = line[2]
                    self.libraries.append(library)
                    self.currLib += 1
                # input line -- the books IDs for previous line library
                else:
                    # modify the last library inserted
                    library = self.libraries[-1]
                    # list with (id, completed, book_score) values
                    library.books = list(zip(line, [False for x in line], [self.bookScores[x] for x in line]))
                    # introduced metrics for each problem
                    library.score = self.get_metrix(library)
                    # sort the books in each library in reverse order
                    library.books.sort(key=lambda tup: tup[2], reverse=True)

                    # initialiaze counters
                    library.current_book = 0
                    library.total_scanned_books = 0
                    library.scanned_books = []

    def get_metrix(self, library):
        prefix = self.infile[0]
        if prefix in 'a':
            library.average = sum(library.books[2]) / len(library.books[2])
            return (library.signup_time / self.D ) * (library.average * library.scans_per_day)
        if prefix in 'bd':
            return (library.signup_time / self.D ) * (library.scans_per_day / library.num_books)
        if prefix in 'c':
            return library.signup_time / self.D
        if prefix in 'e':
            return ((library.num_books * library.scans_per_day) / library.signup_time)
        if prefix in 'f':
            return (library.num_books / library.signup_time)

    def sort_libraries(self):
        if self.infile[0] in 'abcd':
            self.libraries.sort(key=lambda x: x.score)
        elif self.infile[0] in 'ef':
            self.libraries.sort(key=lambda x: x.score, reverse=True)

    def solve(self):
        # sort libraries based on metric and problem
        self.sort_libraries()
        currLibrary = 0
        currentDay = 0
        librariesServing = []
        res_score = 0

        # Algorithm:
        # Serve libraries based on the metric they have been sorted
        #     After the completion of the signup process for the days passed:
        #         Scan books in a Round Robin manner, skipping 0-score and duplicate books
        #         If a library has no books to be scanned anymore:
        #             Remove it from the serving libraries list
        while currentDay < self.D and currLibrary < self.L:
            # print to avoid losing time on uploading
            print(currentDay, currLibrary, self.D, len(self.scanned_books), 'Score =', res_score)
            days_passed = self.libraries[currLibrary].signup_time
            currentDay += days_passed

            self.result_libraries.append(self.libraries[currLibrary])
            self.result_libraries[-1].index = currLibrary
            self.result_libraries[-1].total_scanned_books = 0
            self.result_libraries[-1].scanned_books = []
            librariesServing.append(self.libraries[currLibrary])
            
            librariesToRemove = deque()
            lib_idx = 0
            for lib in librariesServing:
                for j in range(lib.scans_per_day * days_passed):
                    while lib.current_book < lib.num_books:
                        book_id = lib.books[lib.current_book][0]
                        book_score = lib.books[lib.current_book][2]
                        if book_id not in self.scanned_books and book_score > 0:
                            lib.total_scanned_books += 1
                            lib.scanned_books.append(book_id)
                            self.scanned_books.add(book_id)
                            res_score += lib.books[lib.current_book][2]
                            break
                        lib.current_book += 1

                if lib.current_book >= lib.num_books:
                    librariesToRemove.appendleft(lib_idx)
                lib_idx += 1
            
            for idx in librariesToRemove:
                del(librariesServing[idx])

            currLibrary += 1

    def write_file(self, outfile):
        with open(outfile, 'w+') as writer:
            count = 0
            for lib in self.result_libraries:
                if lib.total_scanned_books > 0:
                    count += 1
            writer.write(str(count) + '\n')
            
            for lib in self.result_libraries:
                if lib.total_scanned_books > 0:
                    writer.write(str(lib.id) + ' ' + str(lib.total_scanned_books) + '\n')
                    writer.write(' '.join([str(x) for x in lib.scanned_books]) + '\n')
                        
for infile, outfile in zip(infiles, outfiles):
    problem = Problem()
    problem.read_file(infile)
    problem.solve()
    problem.write_file(outfile)
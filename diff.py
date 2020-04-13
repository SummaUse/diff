# Insert your code in this file


class DiffCommands:


    def __init__(self, filepath):
        self.commands = list()

        with open(f'./{filepath}') as fp:
            for line in fp:
                # __parse() checks each line for possible errors
                self.commands.append(self.__parse(line))

        # but now we need to check the lines together
        for i, command in enumerate(self.commands):

            if i + 1 < len(self.commands):
                c_0 = command
                c_1 = self.commands[i + 1]

                # We would never delete, and then consecutively change
                # or vice versa
                if (c_0.symbol == 'c' and c_1.symbol == 'd') or (c_0.symbol == 'd' and c_1.symbol == 'c'):

                    # Raise if end and start of commands are consecutive
                    if c_0.prefix[1] +  1 == c_1.prefix[0]:
                        raise DiffCommandsError

            # When we remove lines, we must sync up one less than start
            if command.symbol == 'd' and command.prefix[0] != command.suffix[0] + 1:
                raise DiffCommandsError



    def __str__(self):
        return ''.join(self.commands).rstrip()


    def __parse(self, line):
        has_one_a, has_one_d, has_one_c = False, False, False
        command = None

        if 'c' in line:
            has_one_c = line.count('c') == 1
            command = 'c'
        if 'd' in line:
            has_one_d = line.count('d') == 1
            command = 'd'
        if 'a' in line:
            has_one_a = line.count('a') == 1
            command = 'a'

        # Each line should only contain only one command
        if sum([has_one_a, has_one_c, has_one_d]) != 1:
            raise DiffCommandsError

        if ' ' in line:
            raise DiffCommandsError

        # At this point we know there is only one command,
        # that command only appears once, and there are no spaces
        prefix, suffix = line.split(command, 2)

        # Now lets split those up by commas
        prefix = prefix.rstrip().split(',')
        suffix = suffix.rstrip().split(',')

        # This dict tells us how many arguments we can expect 
        # on either side of our command
        constraints = {
            'a': (1, 2),
            'd': (2, 1),
            'c': (2, 2)
        }
        left_max, right_max = constraints[command]

        if not (1 <= len(prefix) <= left_max and 1 <= len(suffix) <= right_max):
            raise DiffCommandsError

        # If we've made it here, it's a valid command
        return Command(command, prefix, suffix)


class Command:
    """ Helper class to store command information in a diff """

    def __init__(self, symbol, psplit, ssplit):
        self.symbol = symbol

        if len(psplit) == 1:
            self.prefix = (int(psplit[0]), int(psplit[0]))
        else:
            self.prefix = tuple(map(int, psplit)) 

        if len(ssplit) == 1:
            self.suffix = (int(ssplit[0]), int(ssplit[0]))
        else:
            self.suffix = tuple(map(int, ssplit))

    
    def __str__(self):
        return f'{self.prefix} {self.symbol} {self.suffix}'


class DiffCommandsError(Exception):
    """ Error is raised when we are unable to parse diff.txt file """
    
    def __init__(self):
        super().__init__('Cannot possibly be the commands for the diff of two files')



class OriginalNewFiles:

    def __init__(self, filepath1, filepath2):

        # Read each file into list of lines
        with open(f'./{filepath1}') as fp:
            file1_lines = [line for line in fp]

        with open(f'./{filepath2}') as fp:
            file2_lines = [line for line in fp]

        # store list of possible lcs for later use
        self.lcs = self.__compute_lcs(file1_lines, file2_lines)


    def __compute_lcs(self, f1, f2):
        """ This func generates LCS as a list of lines """
        x = len(f1) + 1
        y = len(f2) + 1

        # _lcs array contains Pointers that tell us where to look
        _lcs = [ 
            [Pointer(0, []) for _ in range(x)] for _ in range(y) 
        ]

        # Loop through all subsequences
        for i in range(1, y):
            for j in range(1, x):

                # If the characters are not equal we must look up
                # and to the left in our array and compare
                if f1[j - 1] != f2[i - 1]:
                    up_ptr = _lcs[i - 1][j]
                    left_ptr = _lcs[i][j - 1]

                    if up_ptr.length == left_ptr.length:
                        l = up_ptr.length
                        d = ['u', 'l']

                    elif up_ptr.length < left_ptr.length:
                        l = left_ptr.length
                        d = ['l']

                    elif up_ptr.length > left_ptr.length:
                        l = up_ptr.length
                        d = ['u']

                    else:
                        raise RuntimeError(f'LEFT={left_ptr}, UP={up_ptr}')

                # Otherwise they are equal and we look diagnol
                else:
                    p = _lcs[i - 1][j - 1]
                    l = p.length + 1
                    d = ['d']

                # Fill the array with the correct pointer 
                _lcs[i][j] = Pointer(l, d)

        # Now that we have our array of pointers, lets backtrack
        # and generate teh actual subsequences
        return self.__backtrack(_lcs, f1, f2, x - 1, y - 1)


    def __backtrack(self, arr, f1, f2, x, y):
        
        # Recursive base case
        if x == 0 or y == 0:
            return []

        p = arr[y][x]
        new_coordinates = {
            'u': (x, y - 1),
            'd': (x - 1, y - 1),
            'l': (x - 1, y)
        }

        seq = []
        for direction in p.directions:
            x_1, y_1 = new_coordinates[direction]

            returned = self.__backtrack(arr, f1, f2, x_1, y_1)
            seq.extend(returned[:])

            if arr[y_1][x_1].length < p.length:
                seq = seq or [[]]
                for s in seq:
                    s.append(f1[x - 1])
                seq = [s[:] for s in seq]

        return seq


    def output_diff(self):
        pass

    def output_unmodified_from_original(self, diff):
        pass

    def output_unmodified_from_new(self, diff):

        pass

    def get_all_diff_commands(self):
        pass


class Pointer:
    """ Helper class for LCS array """

    def __init__(self, length, directions):
        self.length = length
        self.directions = directions

    def __str__(self):
        return f'({self.length}, {self.directions})'

    def __repr__(self):
        return f'({self.length}, {self.directions})'



if __name__ == "__main__":
    # onf = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
    # print(diff)

    dff = DiffCommands('wrong_6.txt')
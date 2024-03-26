def get_matrix_from_file(lines):
    matrix = []
    for line in lines:
        row = []
        for number in line.split(' '):
            if len(number) > 0:
                row.append(int(number))
        if len(row) > 0:
            matrix.append(row)
    return matrix

def next_multiple_of_eight(number):
    remainder = number % 8
    if remainder == 0:
        # The number is already divisible by 8
        return number
    else:
        # Calculate the next multiple of 8
        next_multiple = number + (8 - remainder)
        return int(next_multiple)
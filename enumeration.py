class Enumeration:
    """
    Helps to make (lightweight) work with custom enum classes easier.
    This class is intended to be subclassed by custom enum classes. Example: class WorkDays(Enumeration)
    Enum values in custom subclass should be defined as class variables, e.g.:
    var1 = "Monday", var2 = 500, var3 = 0.1
    This class doesn't interfere with Python's Enum class namespace, but watch out for typos/confusion.
    """
    _enum_values = []

    @classmethod
    def enum_values(cls, refresh=False):
        """
        Get list of all values in the enum.
        Note: Enum values are loaded only once by default - at first use (enum is not supposed to change
        dynamically). To refresh/load up-to-date values when calling this, use 'refresh' parameter.
        :param refresh - set True to force refresh of current values when calling this method
        :return list of enum values. Example: ['Day', 'Night']
        """
        # load enum values once and save them for future usage (unless forced refresh)
        if refresh or not cls._enum_values:  # if forced refresh or enum values not saved yet, load them
            values = []
            for name, value in cls.__dict__.items():
                if not name.startswith('__'):
                    values.append(value)

            cls._enum_values = values

        return cls._enum_values

    @classmethod
    def contains(cls, item, refresh=False, ignore_case=False):
        """
        Check if given item (value) is contained in enum.
        :param item: check if enum contains this item
        :param refresh: set True to refresh/reload current enum values (if enum changes dynamically)
        :param ignore_case: If True, string item is compared with enum values regardless of lower/upper case
            letters. If False, strings are compared strictly and must have the same case.
        :return True if enum contains the item, False otherwise
        """
        # TODO comparison using unicodedata NFKD normalization
        if (ignore_case is True) and isinstance(item, str):
            item = item.lower()
            for value in cls.enum_values(refresh=refresh):
                if isinstance(value, str) and (item == value.lower()):
                    # item matched a value
                    return True

            # item did not match any value
            return False
        else:
            return True if item in cls.enum_values(refresh=refresh) else False


""" USAGE EXAMPLE """
if __name__ == '__main__':
    # create custom enum class
    class WorkDay(Enumeration):
        mon = 'Monday'
        tue = 'Tuesday'
        wed = 'Wednesday'
        thu = 'Thursday'
        fri = 'Friday'

    # print all items in the enum
    print("Work days are:")
    print(WorkDay.enum_values())

    # check if an item is in the enum
    my_days = ['Sunday', 'Monday', WorkDay.tue]
    for my_day in my_days:
        if my_day in WorkDay.enum_values():
            print("Go to work. It is " + my_day)
        else:
            print("Stay at home. It is " + my_day)

    # check if enum contains an item, ignore lower/upper case letters
    my_day = 'friDAY'
    if WorkDay.contains(my_day, ignore_case=True):
        print("Go to work. It is " + my_day)
    else:
        print("Stay at home. It is " + my_day)

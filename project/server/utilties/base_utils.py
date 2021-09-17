
import os
import re

class base_utils:

    def getMonthandYear(self, text):

        #text = "Exclusive Sale Sales Representative Agreement is made this 10th day of February,2009, by and between OptiCon Systems, Inc., a Nevada, U.S.A. corporationwith its principal place of business at 449 Central Ave, Suite 101, St.Petersburg, FL 33701"

        #text = "New years day was on January 1, 2018, and boy was it a good time!"
        pattern = re.compile(r"""
            [a-z]+  # at least one+ ascii letters (ignore case is use)
            \s      # one space after
            \d\d?   # one or two digits
            ,?      # an oprtional comma
            \s      # one space after
            \d{4}   # four digits (year)
        """, re.IGNORECASE | re.VERBOSE)

        pattern2 = re.compile(r"""
            [a-z]+  # at least one+ ascii letters (ignore case is use)
            ,?      # an oprtional comma
            \d{4}   # four digits (year)
        """, re.IGNORECASE | re.VERBOSE)

        pattern3 = re.compile(r"""
            [a-z]+  # at least one+ ascii letters (ignore case is use)
            \s      # one space after
            \d\d?   # one or two digits
            ,?      # an oprtional comma
            \s      # one space after
            \d{4}   # four digits (year)
        """, re.IGNORECASE | re.VERBOSE)

        result = ""

        if pattern3.search(text):
            result = pattern3.search(text).group()
        elif pattern2.search(text):
            result = pattern2.search(text).group()
        elif pattern.search(text):
            result = pattern.search(text).group()

        # print(result)

        return result
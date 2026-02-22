#!/usr/bin/env python3

# Source - https://stackoverflow.com/a/2257449
# Posted by Ignacio Vazquez-Abrams, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-22, License - CC BY-SA 4.0

import random
import string

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
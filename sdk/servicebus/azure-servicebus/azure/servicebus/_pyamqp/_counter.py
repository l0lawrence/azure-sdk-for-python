#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import time

class TickCounter():
    def __init__(self):
        self._time = time.perf_counter()
    
    def get_current_ms(self):
        # print(time.perf_counter())
        return time.perf_counter()

 
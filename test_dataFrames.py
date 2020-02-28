import os
import pytest
import unittest.mock as mock

import dataFrames as df

def test_create_data_frame():
    assert df.data_frame == True
    if os.path.exists("output.json") :
        os.remove("output.json")
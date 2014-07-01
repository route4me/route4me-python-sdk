#!/usr/bin/python

from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    print 'Reoptimization...'
    optimization_problem_id = 'c46648541ca5d716a31ffae6f405a37d'
    response = route4me.reoptimization(optimization_problem_id)
    print 'Reoptimization status: %s' % \
          OPTIMIZATION_STATE.reverse_mapping.get(response.state)

if __name__ == '__main__':
    main()

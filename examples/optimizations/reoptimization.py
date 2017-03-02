from route4me import Route4Me
from route4me.constants import OPTIMIZATION_STATE

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        optimizations = response.optimizations
        optimization_problem_id = optimizations[0].optimization_problem_id
        print 'Reoptimization problem id: {}'.format(optimization_problem_id)
        response = route4me.reoptimization(optimization_problem_id)
        print 'Reoptimization status: %s' % \
              OPTIMIZATION_STATE.reverse_mapping.get(response.state)

if __name__ == '__main__':
    main()

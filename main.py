import simpy
import random

RANDOM_SEED = 54
SIM_TIME = 480

NUM_DRIVERS = 6

lost_passangers = []
available_drivers = NUM_DRIVERS


def passanger_arrival_time():
    return -0.5 + random.gammavariate(3.72, 1.55)


def service_time():
    return 7.5 + random.gammavariate(2.45, 4.47)


class Katary(object):
    ''' Kataty is the company name. '''

    def __init__(self, env, num_drivers):
        self.env = env
        self.drivers = simpy.Resource(env, capacity=num_drivers)

    def attend(self, name):
        print('%s take the taxi at %.2f.' % (name, self.env.now))
        yield self.env.timeout(service_time())
        print('%s leave the taxi at %.2f.' % (name, self.env.now))


def passenger(env, name, context):

    print('%s requests the service at %.2f.' % (name, env.now))

    if (context.drivers.count == NUM_DRIVERS):
        lost_passangers.append(name)
        return

    with context.drivers.request() as request:
        yield request

        yield env.process(context.attend(name))


def setup(env, num_drivers):

    katary = Katary(env, num_drivers)

    i = 0

    while True:
        yield env.timeout(passanger_arrival_time())
        i += 1
        env.process(passenger(env, 'pasajero %s' % (i), katary))


def main():

    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    env.process(setup(env, NUM_DRIVERS))

    env.run(until=SIM_TIME)

    print('Pasajeros perdidos: %d' % (len(lost_passangers)))


if __name__ == '__main__':
    main()

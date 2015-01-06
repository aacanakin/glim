from glim import paths

paths.configure()

from glim.core import Registry, Facade

registry_config = {
    'a' : 'b',
    'c' : {
        'd' : 'e'
    }
}

# registry tests

def test_registry_init_all():

    registry = Registry(registry_config)

    assert registry_config == registry.registrar
    assert registry_config == registry.all()

def test_registry_get_set():

    registry = Registry(registry_config)

    # ovveride config
    registry.set('a', 'z')
    assert registry.get('a') == 'z'

    registry.set('q', {
        'q1' : 'w1',
        'q2' : 'w2'
    })

    assert registry.get('q.q1') == 'w1'

    registry.set('q.q1', 'wn')

    assert registry.get('q.q1') == 'wn'
    assert registry.get('no-key') == None

def test_registry_flush():

    registry = Registry(registry_config)
    registry.flush()

    assert registry.registrar == {}

def test_registry_update():

    registry = Registry(registry_config)
    registry.update({
        'a' : 'b2',
        'c' : {
            'f' : 'g'
        }
    })

    assert registry.get('a') == 'b2'
    assert registry.get('c.f') == 'g'

# facade tests
class Sample:

    def __init__(self, config={}):
        self.config = config

    def foo(self):
        return 'bar'

class SampleWithMultipleArguments:

    def __init__(self, arg1, arg2, arg3=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def foo(self):
        return '%s,%s,%s bar' % (self.arg1, self.arg2, self.arg3)

class SampleFacade(Facade):

    accessor = Sample

    @classmethod
    def foo_inside_facade(cls):
        return 'bar inside the facade'

class SampleWithMultipleArgumentsFacade(Facade):

    accessor = SampleWithMultipleArguments

    @classmethod
    def foo_inside_facade(cls):
        return 'bar inside the facade'

def test_facade_sample_register():

    sample_config = {
        'a' : 'b'
    }

    sample_config2 = {
        'a' : 'c'
    }

    SampleFacade.register(sample_config)
    assert isinstance(SampleFacade.instance, Sample)
    assert SampleFacade.instance.config == sample_config

    SampleFacade.register(sample_config2)
    assert SampleFacade.instance.config == sample_config

def test_facade_sample_deflect_to_instance():

    sample_config = {
        'a' : 'b'
    }

    SampleFacade.register(sample_config)
    assert SampleFacade.foo() == 'bar'
    assert SampleFacade.foo_inside_facade() == 'bar inside the facade'

def test_facade_sample_wma_boot():

    sample_wma_config = {
        'arg1': 'a1',
        'arg2': 'a2',
        'arg3': 'a3'
    }

    sample_wma_config2 = {
        'arg1': 'b1',
        'arg2': 'b2',
        'arg3': 'b3'
    }

    SampleWithMultipleArgumentsFacade.boot(sample_wma_config['arg1'],
                                           sample_wma_config['arg2'],
                                           sample_wma_config['arg3'])

    assert SampleWithMultipleArgumentsFacade.instance.arg1 == sample_wma_config['arg1']
    assert SampleWithMultipleArgumentsFacade.instance.arg2 == sample_wma_config['arg2']
    assert SampleWithMultipleArgumentsFacade.instance.arg3 == sample_wma_config['arg3']

    SampleWithMultipleArgumentsFacade.boot(sample_wma_config2['arg1'],
                                           sample_wma_config2['arg2'],
                                           sample_wma_config2['arg3'])

    assert SampleWithMultipleArgumentsFacade.instance.arg1 != sample_wma_config2['arg1']
    assert SampleWithMultipleArgumentsFacade.instance.arg2 != sample_wma_config2['arg2']
    assert SampleWithMultipleArgumentsFacade.instance.arg3 != sample_wma_config2['arg3']

def test_facade_sample_wma_deflect_to_instance():

    sample_wma_config = {
        'arg1': 'a1',
        'arg2': 'a2',
        'arg3': 'a3'
    }

    SampleWithMultipleArgumentsFacade.boot(sample_wma_config)
    assert SampleWithMultipleArgumentsFacade.foo() == 'a1,a2,a3 bar'
    assert SampleWithMultipleArgumentsFacade.foo_inside_facade() == 'bar inside the facade'



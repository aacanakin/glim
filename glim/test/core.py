from glim import paths
paths.configure()

from glim.core import Registry

config = {
	'a' : 'b',
	'c' : {
		'd' : 'e'
	}
}

def test_registry_init_all():

	registry = Registry(config)

	assert config == registry.registrar
	assert config == registry.all()

def test_registry_get_set():

	registry = Registry(config)

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
	assert registry.get('c.d') == 'e'
	assert registry.get('no-key') == None

def test_registry_flush():

	registry = Registry(config)
	registry.flush()

	assert registry.registrar == {}

def test_registry_update():

	registry = Registry(config)
	registry.update({
		'a' : 'b',
		'c' : {
			'f' : 'g'
		}
	})

	assert registry.get('c.f') == 'g'


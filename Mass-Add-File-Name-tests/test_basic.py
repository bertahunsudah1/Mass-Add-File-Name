def test_generate():
    from main import generate, sample_schema
    data = generate(sample_schema(), count=2, seed=1)
    assert isinstance(data, list) and len(data) == 2

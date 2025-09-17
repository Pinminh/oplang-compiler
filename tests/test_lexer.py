from utils import Tokenizer


def test_001():
    """Test line comment"""
    source = "# This is good # old ### one-liner # commenter. #"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test line comment"""
    source = "#"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test block comment"""
    source = "/**/"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test block comment"""
    source = "/* FIRST COMMENT \n /* COMMENT ON ANOTHER LINE \n  */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Test line and block comment"""
    source = """
        # This is #first #line ## @#$%TYU 1234546 asdfIQJWE /,[p'l';./] #
        /* This
        is ###!@#$%^& a ./;' block comment./,
        ';l'';l'
        *****/
        # This is final/* line comment # /* */ asdlk
        /********/
        
    """
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
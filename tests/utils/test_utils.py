from app.utils import clean_file_name

def test_clean_file_name():
    assert clean_file_name('Test/Video:Title') == 'Test_Video_Title'
    assert clean_file_name('Another\\Test*Title?') == 'Another_Test_Title_'
    assert clean_file_name('   Title with spaces   ') == 'Title with spaces'
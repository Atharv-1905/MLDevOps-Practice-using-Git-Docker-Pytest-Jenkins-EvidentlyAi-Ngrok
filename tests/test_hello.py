from hello import analyze_marks


def test_student_pass():
    average, result = analyze_marks([35, 45, 23])

    assert average == 103 / 3
    assert result == "Fail"

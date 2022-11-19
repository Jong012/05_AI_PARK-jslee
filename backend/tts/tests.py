from django.test import TestCase

from tts.utils import get_validate_sentence, sentence2texts


class UtilsTest(TestCase):
    def test_get_validate_sentence(self):
        test1 = '@안녕하세요. @하하하#'
        self.assertEqual(get_validate_sentence(test1), '안녕하세요. 하하하')

        test2 = '"안녕하세요." 하하하.'
        self.assertEqual(get_validate_sentence(test2), '"안녕하세요." 하하하.')

        test3 = '$안녕'
        self.assertEqual(get_validate_sentence(test3), '안녕')

    def test_sentence2texts(self):
        test1 = '안녕하세요. 저는 이종성입니다. 반갑습니다! 친하게 지내봅시다'
        self.assertEqual(sentence2texts(test1), ['안녕하세요.', '저는 이종성입니다.', '반갑습니다!', '친하게 지내봅시다'])

        test2 = '.안녕하세요. 저는 이종성입니다. 반갑습니다! 친하게 지내봅시다?'
        self.assertEqual(sentence2texts(test2), ['.', '안녕하세요.', '저는 이종성입니다.', '반갑습니다!', '친하게 지내봅시다?'])

        test3 = '안녕하세요'
        self.assertEqual(sentence2texts(test3), ['안녕하세요'])

        test4 = '안녕하세요. 저는 이종성입니다. 반갑습니다! 친하게 지내봅시다?'
        self.assertEqual(sentence2texts(test4), ['안녕하세요.', '저는 이종성입니다.', '반갑습니다!', '친하게 지내봅시다?'])

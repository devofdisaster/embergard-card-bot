from discord.email_helper import EmailParser


class TestEmailParser:
    """Test cases for the EmailParser class."""

    def test_parse_valid_email_request(self):
        """Test parsing a valid email request."""
        message = """[[Bug Report: Card Display Issue]]
I found a problem with the card display when searching for certain cards.
The thumbnail doesn't load properly.

Steps to reproduce:
1. Search for specific card
2. Notice the missing thumbnail"""

        result = EmailParser.parse_email_request(message)
        assert result is not None
        subject, body = result
        assert subject == "Bug Report: Card Display Issue"
        assert "I found a problem" in body
        assert "Steps to reproduce" in body

    def test_parse_email_request_with_extra_whitespace(self):
        """Test parsing email request with extra whitespace in brackets."""
        message = """[[  Suggestion: New Feature  ]]
This is my suggestion for a new feature."""

        result = EmailParser.parse_email_request(message)
        assert result is not None
        subject, body = result
        assert subject == "Suggestion: New Feature"
        assert body == "This is my suggestion for a new feature."

    def test_parse_email_request_multiline_body(self):
        """Test parsing email request with multiline body."""
        message = """[[Feature Request]]
Line 1 of content
Line 2 of content
Line 3 of content"""

        result = EmailParser.parse_email_request(message)
        assert result is not None
        subject, body = result
        assert subject == "Feature Request"
        assert "Line 1 of content\nLine 2 of content\nLine 3 of content" == body

    def test_parse_invalid_email_request_no_subject(self):
        """Test parsing invalid email request with no subject."""
        message = """[[]]
This has no subject."""

        result = EmailParser.parse_email_request(message)
        assert result is None

    def test_parse_invalid_email_request_no_body(self):
        """Test parsing invalid email request with no body."""
        message = """[[Subject Only]]"""

        result = EmailParser.parse_email_request(message)
        assert result is None

    def test_parse_no_email_pattern(self):
        """Test parsing message without email pattern."""
        message = """This is just a regular message without email format."""

        result = EmailParser.parse_email_request(message)
        assert result is None

    def test_parse_card_search_pattern(self):
        """Test that card search patterns are not parsed as email."""
        message = """((ghartok))"""

        result = EmailParser.parse_email_request(message)
        assert result is None

    def test_generate_mailto_link_basic(self):
        """Test generating a basic mailto link."""
        subject = "Test Subject"
        body = "Test body content"

        result = EmailParser.generate_mailto_link(subject, body)
        expected = "mailto:whunderworlds@gwplc.com?subject=Test%20Subject&body=Test%20body%20content"
        assert result == expected

    def test_generate_mailto_link_with_special_characters(self):
        """Test generating mailto link with special characters."""
        subject = "Bug: Card & Deck Issues"
        body = "This is a test with special chars: @#$%^&*()"

        result = EmailParser.generate_mailto_link(subject, body)
        assert "whunderworlds@gwplc.com" in result
        assert "subject=Bug%3A%20Card%20%26%20Deck%20Issues" in result
        assert "%40%23%24%25%5E%26%2A%28%29" in result  # URL encoded special chars

    def test_generate_mailto_link_with_newlines(self):
        """Test generating mailto link with newlines in body."""
        subject = "Multi-line Report"
        body = "Line 1\nLine 2\nLine 3"

        result = EmailParser.generate_mailto_link(subject, body)
        assert "whunderworlds@gwplc.com" in result
        assert "Line%201%0ALine%202%0ALine%203" in result  # URL encoded newlines

    def test_process_email_request_valid(self):
        """Test complete email request processing."""
        message = """[[Test Subject]]
Test body content"""

        result = EmailParser.process_email_request(message)
        assert result is not None
        assert "mailto:whunderworlds@gwplc.com" in result
        assert "subject=Test%20Subject" in result
        assert "body=Test%20body%20content" in result

    def test_process_email_request_invalid(self):
        """Test complete email request processing with invalid input."""
        message = """This is not an email request"""

        result = EmailParser.process_email_request(message)
        assert result is None

    def test_recipient_email_constant(self):
        """Test that the recipient email is correct."""
        assert EmailParser.RECIPIENT_EMAIL == "whunderworlds@gwplc.com"

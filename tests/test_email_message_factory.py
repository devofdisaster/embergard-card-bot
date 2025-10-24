from src.discord.message_factory import generate_email_embed


class TestEmailMessageFactory:
    """Test cases for email-related message factory functions."""

    def test_generate_email_embed_basic(self):
        """Test generating a basic email embed."""
        subject = "Test Subject"
        body = "Test body content"
        mailto_link = (
            "mailto:test@example.com?subject=Test%20Subject&body=Test%20body%20content"
        )

        embed = generate_email_embed(subject, body, mailto_link)

        assert embed.title == "📧 Email to Warhammer Underworlds Team"
        assert "whunderworlds@gwplc.com" in embed.description
        assert embed.color.value == 0x3498DB

        # Check fields
        assert len(embed.fields) == 3
        assert embed.fields[0].name == "Subject"
        assert subject in embed.fields[0].value
        assert embed.fields[1].name == "Message"
        assert body in embed.fields[1].value
        assert embed.fields[2].name == "📎 Send Email"
        assert mailto_link in embed.fields[2].value

        assert embed.footer.text == "This will open your default email application"

    def test_generate_email_embed_long_body(self):
        """Test generating email embed with long body that gets truncated."""
        subject = "Test Subject"
        body = "A" * 1000  # Very long body
        mailto_link = "mailto:test@example.com"

        embed = generate_email_embed(subject, body, mailto_link)

        # Body should be truncated
        body_field = embed.fields[1]
        assert "..." in body_field.value
        assert (
            len(body_field.value) < len(body) + 20
        )  # Should be much shorter than original

    def test_generate_email_embed_multiline_body(self):
        """Test generating email embed with multiline body."""
        subject = "Multi-line Subject"
        body = "Line 1\nLine 2\nLine 3"
        mailto_link = "mailto:test@example.com"

        embed = generate_email_embed(subject, body, mailto_link)

        # Check that newlines are preserved
        body_field = embed.fields[1]
        assert "Line 1" in body_field.value
        assert "Line 2" in body_field.value
        assert "Line 3" in body_field.value

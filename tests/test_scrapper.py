import pytest
from unittest.mock import Mock, patch
from wechat_scrapper.scrapper import WechatScrapper


@pytest.fixture
def mock_dependencies():
    """Create mock objects for all dependencies of WechatScrapper."""
    mock_articles_info = Mock()
    mock_url2html = Mock()
    mock_public_accounts_web = Mock()
    mock_url2pdf = Mock()
    mock_html2md = Mock()

    with patch(
        'wechat_scrapper.scrapper.ArticlesInfo', return_value=mock_articles_info
    ), patch('wechat_scrapper.scrapper.Url2Html', return_value=mock_url2html), patch(
        'wechat_scrapper.scrapper.PublicAccountsWeb',
        return_value=mock_public_accounts_web,
    ), patch(
        'wechat_scrapper.scrapper.Url2Pdf', return_value=mock_url2pdf
    ), patch(
        'wechat_scrapper.scrapper.Html2Markdown', return_value=mock_html2md
    ):
        scrapper = WechatScrapper(appmsg_token="test_token", cookie="test_cookie")

        yield {
            'scrapper': scrapper,
            'articles_info': mock_articles_info,
            'url2html': mock_url2html,
            'public_accounts_web': mock_public_accounts_web,
            'url2pdf': mock_url2pdf,
            'html2md': mock_html2md,
        }


class TestWechatScrapper:
    def test_init(self, mock_dependencies):
        """Test that the WechatScrapper initializes correctly."""
        scrapper = mock_dependencies['scrapper']
        assert scrapper is not None
        assert scrapper.articles_info is mock_dependencies['articles_info']
        assert scrapper.url2html is mock_dependencies['url2html']
        assert scrapper.public_accounts_web is mock_dependencies['public_accounts_web']
        assert scrapper.url2pdf is mock_dependencies['url2pdf']
        assert scrapper.html2md is mock_dependencies['html2md']

    def test_download_with_url(self, mock_dependencies):
        """Test download method with a URL."""
        scrapper = mock_dependencies['scrapper']
        mock_url2html = mock_dependencies['url2html']

        test_url = "https://test.com/article"
        mock_url2html.run.return_value = "<html>Test content</html>"

        result = scrapper.download(url=test_url)

        mock_url2html.run.assert_called_once_with(test_url, 4)
        assert result == "<html>Test content</html>"

    def test_download_with_nickname(self, mock_dependencies):
        """Test download method with a nickname."""
        scrapper = mock_dependencies['scrapper']
        scrapper.download_articles = Mock()
        test_nickname = "test_nickname"

        scrapper.download(nickname=test_nickname, format="pdf")

        scrapper.download_articles.assert_called_once_with(test_nickname, "pdf")

    def test_download_article(self, mock_dependencies):
        """Test download_article method."""
        scrapper = mock_dependencies['scrapper']
        mock_url2html = mock_dependencies['url2html']

        test_url = "https://test.com/article"
        mock_url2html.run.return_value = "<html>Test content</html>"

        result = scrapper.download_article(test_url, 2)

        mock_url2html.run.assert_called_once_with(test_url, 2)
        assert result == "<html>Test content</html>"

    def test_get_article_info(self, mock_dependencies):
        """Test get_article_info method."""
        scrapper = mock_dependencies['scrapper']
        mock_articles_info = mock_dependencies['articles_info']

        test_url = "https://test.com/article"
        expected_info = {"title": "Test Article", "author": "Test Author"}
        mock_articles_info.content.return_value = expected_info

        result = scrapper.get_article_info(test_url)

        mock_articles_info.content.assert_called_once_with(test_url)
        assert result == expected_info

    def test_get_public_account_info(self, mock_dependencies):
        """Test get_public_account_info method."""
        scrapper = mock_dependencies['scrapper']
        mock_public_accounts_web = mock_dependencies['public_accounts_web']

        test_nickname = "test_nickname"
        expected_info = {"name": "Test Account", "description": "Test Description"}
        mock_public_accounts_web.official_info.return_value = expected_info

        result = scrapper.get_public_account_info(test_nickname)

        mock_public_accounts_web.official_info.assert_called_once_with(test_nickname)
        assert result == expected_info

    def test_get_all_article_urls(self, mock_dependencies):
        """Test get_all_article_urls method."""
        scrapper = mock_dependencies['scrapper']
        mock_public_accounts_web = mock_dependencies['public_accounts_web']

        test_nickname = "test_nickname"
        first_batch = [
            {"link": "https://test.com/article1"},
            {"link": "https://test.com/article2"},
            {"link": "https://test.com/article3"},
        ]
        second_batch = [
            {"link": "https://test.com/article4"},
            {"link": "https://test.com/article5"},
        ]
        third_batch = []

        mock_public_accounts_web.get_urls.side_effect = [
            first_batch,
            second_batch,
            third_batch,
        ]

        result = scrapper.get_all_article_urls(test_nickname)

        assert mock_public_accounts_web.get_urls.call_count == 3
        mock_public_accounts_web.get_urls.assert_any_call(
            test_nickname, begin=0, count=5
        )
        mock_public_accounts_web.get_urls.assert_any_call(
            test_nickname, begin=5, count=5
        )
        mock_public_accounts_web.get_urls.assert_any_call(
            test_nickname, begin=10, count=5
        )

        expected_urls = [
            "https://test.com/article1",
            "https://test.com/article2",
            "https://test.com/article3",
            "https://test.com/article4",
            "https://test.com/article5",
        ]
        assert result == expected_urls

    def test_download_articles_html_format(self, mock_dependencies):
        """Test download_articles method with HTML format."""
        scrapper = mock_dependencies['scrapper']
        test_urls = ["https://test.com/article1", "https://test.com/article2"]
        scrapper.get_all_article_urls = Mock(return_value=test_urls)
        scrapper.download_article = Mock()

        scrapper.download_articles("test_nickname", format="html")

        scrapper.get_all_article_urls.assert_called_once_with("test_nickname")
        assert scrapper.download_article.call_count == 2
        scrapper.download_article.assert_any_call("https://test.com/article1", mode=4)
        scrapper.download_article.assert_any_call("https://test.com/article2", mode=4)

    def test_download_articles_pdf_format(self, mock_dependencies):
        """Test download_articles method with PDF format."""
        scrapper = mock_dependencies['scrapper']
        mock_url2pdf = mock_dependencies['url2pdf']

        test_urls = ["https://test.com/article1", "https://test.com/article2"]
        scrapper.get_all_article_urls = Mock(return_value=test_urls)

        scrapper.download_articles("test_nickname", format="pdf")

        scrapper.get_all_article_urls.assert_called_once_with("test_nickname")
        assert mock_url2pdf.url_to_pdf.call_count == 2
        mock_url2pdf.url_to_pdf.assert_any_call(
            "https://test.com/article1", title="article1"
        )
        mock_url2pdf.url_to_pdf.assert_any_call(
            "https://test.com/article2", title="article2"
        )

    def test_download_articles_markdown_format(self, mock_dependencies):
        """Test download_articles method with Markdown format."""
        scrapper = mock_dependencies['scrapper']
        mock_html2md = mock_dependencies['html2md']

        test_urls = ["https://test.com/article1", "https://test.com/article2"]
        scrapper.get_all_article_urls = Mock(return_value=test_urls)
        scrapper.download_article = Mock(
            side_effect=["<html>Content 1</html>", "<html>Content 2</html>"]
        )

        scrapper.download_articles("test_nickname", format="markdown")

        scrapper.get_all_article_urls.assert_called_once_with("test_nickname")
        assert scrapper.download_article.call_count == 2
        scrapper.download_article.assert_any_call("https://test.com/article1", mode=1)
        scrapper.download_article.assert_any_call("https://test.com/article2", mode=1)

        assert mock_html2md.convert.call_count == 2
        mock_html2md.convert.assert_any_call("<html>Content 1</html>", title="article1")
        mock_html2md.convert.assert_any_call("<html>Content 2</html>", title="article2")

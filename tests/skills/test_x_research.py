"""x-research/scripts/x_research.py の単体テスト"""
import pytest


class TestImport:
    def test_import_module(self):
        import x_research
        assert hasattr(x_research, 'QueryBuilder')
        assert hasattr(x_research, 'ReportGenerator')
        assert hasattr(x_research, 'sanitize_filename')


class TestQueryBuilder:
    def test_basic_keyword(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI")
        assert qb.build() == "AI"

    def test_with_lang(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").lang("ja")
        assert qb.build() == "AI lang:ja"

    def test_lang_all_ignored(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").lang("all")
        assert qb.build() == "AI"

    def test_exclude_retweets(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").exclude_retweets()
        assert "-is:retweet" in qb.build()

    def test_exclude_replies(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").exclude_replies()
        assert "-is:reply" in qb.build()

    def test_has_media(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").has_media()
        assert "has:media" in qb.build()

    def test_from_user(self):
        from x_research import QueryBuilder
        qb = QueryBuilder("AI").from_user("testuser")
        assert "from:testuser" in qb.build()

    def test_chaining(self):
        from x_research import QueryBuilder
        query = (
            QueryBuilder("Claude AI")
            .lang("en")
            .exclude_retweets()
            .exclude_replies()
            .build()
        )
        assert "Claude AI" in query
        assert "lang:en" in query
        assert "-is:retweet" in query
        assert "-is:reply" in query


class TestSanitizeFilename:
    def test_basic(self):
        from x_research import sanitize_filename
        assert sanitize_filename("hello world") == "hello_world"

    def test_special_chars(self):
        from x_research import sanitize_filename
        result = sanitize_filename('test<>:"/\\|?*file')
        assert "<" not in result
        assert ">" not in result
        assert '"' not in result

    def test_truncation(self):
        from x_research import sanitize_filename
        result = sanitize_filename("a" * 200)
        assert len(result) <= 80

    def test_empty_string(self):
        from x_research import sanitize_filename
        assert sanitize_filename("") == "unnamed"

    def test_strip_dots_underscores(self):
        from x_research import sanitize_filename
        result = sanitize_filename("...test...")
        assert not result.startswith(".")
        assert not result.endswith(".")


class TestReportGenerator:
    @pytest.fixture
    def sample_tweets(self):
        return [
            {
                "id": "1",
                "text": "Hello world #AI",
                "author_id": "u1",
                "created_at": "2026-01-15T10:00:00Z",
                "public_metrics": {
                    "like_count": 100,
                    "retweet_count": 50,
                    "reply_count": 10,
                },
                "entities": {
                    "hashtags": [{"tag": "AI"}],
                    "urls": [],
                },
            },
            {
                "id": "2",
                "text": "Another tweet",
                "author_id": "u2",
                "created_at": "2026-01-16T12:00:00Z",
                "public_metrics": {
                    "like_count": 200,
                    "retweet_count": 30,
                    "reply_count": 5,
                },
                "entities": {
                    "hashtags": [{"tag": "AI"}, {"tag": "Tech"}],
                },
            },
        ]

    @pytest.fixture
    def sample_users(self):
        return [
            {"id": "u1", "username": "user1", "name": "User One",
             "public_metrics": {"followers_count": 1000}},
            {"id": "u2", "username": "user2", "name": "User Two",
             "public_metrics": {"followers_count": 5000}},
        ]

    @pytest.fixture
    def report(self, sample_tweets, sample_users):
        from x_research import ReportGenerator
        return ReportGenerator(
            tweets=sample_tweets,
            users=sample_users,
            meta={"result_count": 2},
            query="AI",
            params={"topic": "AI", "lang": "ja"},
        )

    def test_calculate_stats(self, report):
        stats = report._calculate_stats()
        assert stats["total_tweets"] == 2
        assert stats["unique_authors"] == 2
        assert stats["total_likes"] == 300
        assert stats["total_retweets"] == 80
        assert stats["total_replies"] == 15
        assert stats["avg_likes"] == 150.0

    def test_extract_hashtags(self, report):
        hashtags = report._extract_hashtags()
        assert hashtags["AI"] == 2
        assert hashtags["Tech"] == 1

    def test_analyze_timeline(self, report):
        timeline = report._analyze_timeline()
        assert "2026-01-15" in timeline
        assert "2026-01-16" in timeline

    def test_rank_tweets(self, report):
        top = report._rank_tweets("like_count", 1)
        assert len(top) == 1
        assert top[0]["id"] == "2"  # 200 likes > 100 likes

    def test_generate_markdown(self, report):
        md = report.generate_markdown(top_n=2)
        assert "X Research Report" in md
        assert "user1" in md
        assert "user2" in md

    def test_generate_text(self, report):
        txt = report.generate_text()
        assert "X Research" in txt
        assert "@user1" in txt

    def test_generate_json(self, report):
        data = report.generate_json()
        assert "stats" in data
        assert "tweets" in data
        assert len(data["tweets"]) == 2

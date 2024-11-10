# import libraries
from flask import Flask, render_template, request
from newsapi import NewsApiClient

# init flask app
app = Flask(__name__)

# Init news api 
newsapi = NewsApiClient(api_key='61cb587f85604ee6b51a99fff53ed957')

# helper function to filter out articles from "removed.com"
def exclude_domains(articles, excluded_domains):
    filtered_articles = []
    for article in articles:
        if not any(domain in article['url'] for domain in excluded_domains):
            filtered_articles.append(article)
    return filtered_articles

@app.route("/", methods=['GET', 'POST'])
def home():
    excluded_domains = ["removed.com"] 
    keyword = "mental wellness"  # Default keyword for news
    
    if request.method == "POST":
        keyword = request.form.get("keyword", "mental wellness")  # Use form input or default to "mental health"
    
    related_news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy', page_size=50)
    no_of_articles = min(related_news['totalResults'], 50)  # Limit to 50 articles
    all_articles = related_news['articles'][:no_of_articles]

    # Exclude specific domains
    all_articles = exclude_domains(all_articles, excluded_domains)

    return render_template("home.html", all_articles=all_articles, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)

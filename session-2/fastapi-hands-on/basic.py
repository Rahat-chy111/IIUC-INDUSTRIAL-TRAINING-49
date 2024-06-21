from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()


news = {
    1:
    {
        "id": 1,
        "title": "The Formation of the Avengers: Earth's Mightiest Heroes",
        "content": "A look into how the Avengers were formed, bringing together a team of superheroes to protect Earth.",
        "author": "Nick Fury"
    },
    2:
    {
        "id": 2,
        "title": "Iron Man: The Genius, Billionaire, Playboy, Philanthropist",
        "content": "Exploring the journey of Tony Stark from a billionaire playboy to the armored hero, Iron Man.",
        "author": "Pepper Potts"
    },
    3:
    {
        "id": 3,
        "title": "The Legacy of Captain America",
        "content": "The story of Steve Rogers, the super-soldier who became the symbol of hope and justice as Captain America.",
        "author": "Bucky Barnes"
    },
    4:
    {
        "id": 4,
        "title": "The Incredible Hulk: Strength and Struggle",
        "content": "An analysis of Bruce Banner's transformation into the Hulk and his struggle to control his immense power.",
        "author": "Betty Ross"
    },
    5:
    {
        "id": 5,
        "title": "The Enigmatic Black Widow",
        "content": "Delving into the past and skills of Natasha Romanoff, the Black Widow, and her role in the Avengers.",
        "author": "Clint Barton"
    },
    6:
    {
        "id": 6,
        "title": "Thor: The God of Thunder",
        "content": "Exploring Thor's journey from Asgardian prince to Avenger, and his battles to protect both Earth and Asgard.",
        "author": "Jane Foster"
    },
    7:
    {
        "id": 7,
        "title": "Hawkeye: The Sharpest Shooter",
        "content": "A closer look at Clint Barton, the master archer known as Hawkeye, and his contributions to the Avengers.",
        "author": "Laura Barton"
    },
    8:
    {
        "id": 8,
        "title": "The Rise of the Scarlet Witch",
        "content": "Exploring Wanda Maximoff's transformation into the Scarlet Witch and her powerful abilities.",
        "author": "Vision"
    },
    9:
    {
        "id": 9,
        "title": "Vision: The Synthetic Avenger",
        "content": "The creation and evolution of Vision, the android Avenger with a mind and heart of his own.",
        "author": "Wanda Maximoff"
    },
    10:
    {
        "id": 10,
        "title": "The Battle of New York: The Avengers' First Test",
        "content": "An in-depth look at the Battle of New York, where the Avengers first united to defend Earth from alien invasion.",
        "author": "Phil Coulson"
    }

}


class News(BaseModel):
    title: str
    content: str | None = None
    author: str


@app.get("/")
def hearbeat():
    return {"message": "I'm up and running and shouting!"}

@app.get("/news")
def all_news():
    return news


@app.get("/news")
def news_by_title(title_contains: str):
    print(title_contains)
    for single_news in news.values():
        if title_contains.lower() in single_news["title"].lower():
            return single_news

    return {"data": "No news found with title containing "+title_contains}


# http://localhost:8000/news/%7Bauthor%7D?title_contains=llm
@app.get("/news/{author}")
def news_filter_by_author_title(author: str, title_contains: str = None):
    print(author, title_contains)
    filtered_news = [news for news in news.values() if news["author"].lower() == author.lower()]
    print(filtered_news)
    if title_contains:
        filtered_news = [news for news in filtered_news if title_contains.lower() in news["title"].lower()]
        if not filtered_news:
            return {"data": f"No news found from author {author} with title containing {title_contains}"}
    return filtered_news



@app.get("/news/{id}")
def news_by_id(id: int):
    if id not in news:
        return {"error": f"News with id {id} not found"}
    return news[id]


@app.post("/create-news")
def create_news(response_news: News):
    print(response_news)

    id = max(news.keys()) + 1
    news[id] = {
        "id": id,
        "title": response_news.title,
        "content": response_news.content,
        "author": response_news.author
    }

    return news[id]

if __name__ == '__main__':
    uvicorn.run("basic:app", host='localhost', port=8000, reload=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.urls import url_route

app = FastAPI(
title="Event-Management",
              docs_url='/',
              description='An Application for managing the events',
              contact={'name':'Event Management',
                        'email':'revanthatmakuru98@gmail.com'},
              version="0.0.1",
              license_info={"name": "Apache 2.0",
                            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",},)

app.include_router(url_route)

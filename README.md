
# Music Recommendation based on user’s current emotion

05506210 AI class project
## Project Members
......

## Requirements
- have [Python](https://www.python.org/) installed
- have [Git](https://git-scm.com/) installed (optional)

## How To Run Project

### Clone Project

```bash
git clone https://github.com/luxifearzz/music-recommendation-by-emotion-detection.git
```

### download neccessary files

#### download music (thai, english) from : 
- https://drive.google.com/drive/folders/1-88pvFKC9FNeW-kpqIZ5hgALeAXbKu2u
- paste in folder ```backend/my_flask_api/music/``` (same place as ```.paste_thai_non-thai_here```)
- rename ```english``` folder to ```non-thai```

#### download model.h5 file from :
- https://drive.google.com/file/d/1Z5fJ6hz38DyWrN9mg817sWInloWUh-Zr/view?usp=sharing
- paste in folder ```backend/my_flask_api/models/``` (same place as ```.paste_model.h5_here```)

### run backend server

open terminal at root folder of project and run this command

```bash
cd backend/my_flask_api
py app.py
```

### run frontend server

open terminal at root folder of project and run this command

```bash
python -m http.server -d frontend/
```

### usage

- open web browser
- type ```localhost:8000``` in the address bar
- ready to go

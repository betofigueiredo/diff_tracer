<h1 align="center">DIFF TRACER</h1>
<p align="center">
  Compare two responses to see if there is any difference or if both are having identical properties and values.
  <br/><br/>
  <a href="https://github.com/betofigueiredo/diff_tracer/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&labelColor=363a4f&color=a6da95"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&labelColor=363a4f&color=346FA0"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Made%20with-FastAPI-blue?style=for-the-badge&labelColor=363a4f&color=009485"></a>
  <br/><br/>
</p>

> [!WARNING]
> Please keep in mind that Diff Tracer is still under active development

<h2>Installation</h2>

<p>work is progress...</p>

<h2>Known issues</h2>

<p>
- The files are saved local on your API, so everytime you make a new deploy they will be erased.
</p>

<h2>Contributing</h2>

<p>
For local development just install the libraries and start the FastAPI example file:

```zsh
❯ poetry install
❯ poetry run task start_api
```

Access http://localhost:8000/users to simulate requests.

Access http://localhost:8000/diff-tracer-view/1234 to view de dashboard. 1234 is the default token.

<br />

To run the tests:

```zsh
❯ poetry run task test
```

<br />

Call Integrator endpoint to fetch data from API:

```zsh
❯ curl http://localhost:3002/get-users
```

</p>

<h2>Thanks to</h2>

The code that makes the comparison is from Google Diff, Match and Patch Library written by Neil Fraser Copyright (c) 2006 Google Inc. http://code.google.com/p/google-diff-match-patch/

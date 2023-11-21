# II2202 - Research Methodology and Scientific Writing

This project aims to make a comparison between WebSockets and GraphQL Subscriptions in terms of performance and scalability. The idea behind this project is to find out how GraphQL Subscriptions in its current form is in terms of performance and scalability compared to a pure WebSockets applications for **real-time applications**.

## Authors
- [Eashin Mattuber](https://github.com/eeashin)
- [Enric Perpinyà](https://github.com/evilmonkey19)

## Project Structure
There are two main folders in this project:
- `websockets`: Contains the code for the WebSockets application.
- `graphql`: Contains the code for the GraphQL application.

Both applications are compared using different metrics provided by K6S. The results are stored in the `results` folder.
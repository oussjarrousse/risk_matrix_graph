# Generate-risk-matrix-graph

## Installation

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt`

##csv file format:

* The csv file must contain a headeere with at least the following columns:
  - id
  - impact
  - likelihood
  - simple_risk
  
  The header could have more columns. The order of columns is not relevant.

* Values for the "impact", and "likelihood" must be numbers between 0 and 5

* simple_risk = impact x likelihood, so between 0 and 25. It affects the radius of points on the graph.

check the provided *.csv files in the examples folder

## Usage

    $ python3 generate_risk_matrix_graph examples/data_1.csv output_1.png

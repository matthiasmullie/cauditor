# Codecharts

So, I don't really know any Python but I wanted to give it a go for this project. It will be bad!

That said, let's quickly go over it all:

## index.py

Web request entrypoint.

Instances of all controllers.*.Controller objects will be created.
Controllers will throw an exception if they're not suited for this request.
The controller returning the highest value for `.match()` will be rendered.

## controllers/*

Controllers for all web requests.

`__init__` will receive `os.environ["REQUEST_URI"]` and either correctly instantiate, or throw an exception if it's not
suited to handle this request. Exception should be thrown as early as possible (if the regex doesn't even match, don't
do any DB-lookup) because we'll instantiate every controller. `__init__` should fail fast!

.match() will return a re.match result for the relevant portion of the uri that was matched.
.args() will return all arguments needed to render the template.
.headers() will return HTTP headers to be output
.render() will return the parsed template indicated by `self.template` (in templates/*)
.cookie() can be used to get and set data from/to cookie
.session() can be used to get and set data from/to session

There will always be at least 1 matching controller object: fallback.py matches everything and will render a 404.

## models/*

Extremely simple database-interaction handlers.

Allows for simple select, upsert & delete.

## import/*

Import-related scripts will be shoved in here. Makefile will orchestrate everything.

## templates/*

jinja2 templates

controllers/* will reference these files (as `self.template`) & they will be fed all the arguments that the controller's
`.args()` returns.

## assets/

### assets/css/*

Whatever CSS is needed...

### assets/js/*

Charts will be drawn using [d3.js](http://d3js.org/) and [d3plus.js](http://d3plus.org/), which are in data/js/vendor/*

data/js/Codecharts.js is an easy entrypoint to draw the charts.
`Codecharts` takes the path to a JSON data file in the constructor.
`.draw` takes a selector (element to draw the chart to) and a visualization object.

All of the chart types have their own constructors:
data/js/visualizations/Abstract.js is the abstract class that all vizualizations should inherit from.

Currently, the only chart type is a treemap, so all charts are in data/js/visualizations/treemap/*, where
Abstract.js defines the shared treemap-type code among all these type of charts.
Method.js adds some additional info for the charts that have data on method-level.
Class.js adds some additional info for the charts that have data on class-level.

All other files contain specific details for that specific chart. This will be very little, since most of the code will
already be in (Method|Class).js, which they extend from, or Abstract.js, or that other Abstract.js.

## data/*

JSON files holding the metrics.

Files will be stored in data/[vendor]/[project]/[commit-sha].json

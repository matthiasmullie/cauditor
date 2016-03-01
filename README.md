# cauditor.org

So, I don't really know any Python but I wanted to give it a go for this project. It will be bad!

That said, let's quickly go over it all:

## controllers/*

Controllers for all web requests.

`__init__.py` has a method `route()` that accepts `os.environ["REQUEST_URI"]` and returns the controller (based on
`controllers.routes` `{regex: controller}` mapping. The regex must extract all of the controller's `__init__` arguments
as named subpatterns.

The controller can still fail on `__init__()`, in which case the next matched controller will be
tried. Exceptions should be thrown as early as possible (if the regex doesn't even match, don't
do any DB-lookup) because we'll instantiate every controller. `__init__` should fail fast!

* `match()` will return a re.match result for the relevant portion of the uri that was matched.
* `args()` will return all arguments needed to render the template.
* `headers()` will return HTTP headers to be output
* `render()` will return the parsed template indicated by `self.template` (in templates/*)
* `cookie()` can be used to get and set data from/to cookie
* `session()` can be used to get and set data from/to session

There will always be at least 1 matching controller object: fallback.py matches everything and will render a 404.

## models/*

Extremely simple database-interaction handlers.

Allows for simple select, upsert, update & delete.

Session handler (sessions.py) is in here too (they use DB)

## listeners/*

After analyzing commits, the result will be passed off to these files, who can then further process that data.

* `store_file.py` will store the result to a json file
* `store_db.py` will record the commit in DB along with metric differences between commits

## templates/*

jinja2 templates

`container.html` is the "master template" inside which all controller-specific templates will be rendered.

controllers/* will reference these files (as `self.template`) & they will be fed all the arguments that the controller's
`.args()` returns.

## assets/

### assets/css/*

Whatever CSS is needed...

### assets/js/*

Charts will be drawn using [d3.js](http://d3js.org/) and [d3plus.js](http://d3plus.org/), which are in data/js/vendor/*

assets/js/Cauditor.js is an easy entrypoint to draw the charts.
`Cauditor` takes the path to a visualization in the constructor.
`.draw` takes a selector (element to draw the chart to) and a visualization object.

All of the chart types have their own constructors:
assets/js/visualizations/Abstract.js is the abstract class that all vizualizations should inherit from.
They'll take a Cauditor.Data object in the constructor.

Currently, the only chart type is a treemap, so all charts are in data/js/visualizations/treemap/*, where
Abstract.js defines the shared treemap-type code among all these type of charts.
Method.js adds some additional info for the charts that have data on method-level.
Class.js adds some additional info for the charts that have data on class-level.

All other files contain specific details for that specific chart. This will be very little, since most of the code will
already be in (Method|Class).js, which they extend from, or Abstract.js, or that other Abstract.js.

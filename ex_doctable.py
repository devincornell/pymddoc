
import pymddoc

document = pymddoc.Document(
    metadata = pymddoc.Metadata.new(
        title = 'My Test Document',
        subtitle = 'A test document for pymddoc',
        id = 'my-test-document',
        author = 'Devin J. Cornell',
        date = '2021-09-10',
    ),
    snippet_template = pymddoc.templates.default(),
)

document.markdown('''

# Basics of `doctable`

In this brief tutorial, we will cover the basics of doctable. We will cover the following topics:

+ Connecting to the database using `ConnectCore`.
+ Defining a database schema using the `table_schema` decorator.
+ Creating the table using the `begin_ddl()` context manager.
+ Inserting values into the database using the `ConnectQuery` and `ConnectTable` interfaces.

''')

import sys
sys.path.append('..')

import doctable

@document.snippet
def load():
    import doctable

document.markdown('''

The ConnectCore objects acts as the primary starting point for any actions performed on the database. We create a new connection to the datbase using the .open() factory method constructor.

''')

core = None

@document.snippet
def connect():
    global core
    core = doctable.ConnectCore.open(
        target=':memory:', 
        dialect='sqlite'
    )
    return core

document.markdown('''

Next we define a very basic schema using the `table_schema` decorator. This decorator is used to create a `Container` object, which contains information about the database schema and is also a dataclass that can be inserted or retrieved from the database. Read the schema definition examples for more information on creating container objects and database schemas.

''')

MyContainer0 = None

@document.snippet
def another():
    global MyContainer0
    
    @doctable.table_schema
    class MyContainer0:
        id: int
        name: str
        age: int

    return doctable.inspect_schema(MyContainer0).column_info_df()


document.markdown('''

We actually connect to the database table using the context manager returned by .begin_ddl(). This design is necessary for multi-table schemas, but, because of the readability it provides, I will use it for single-table schemas as well. The method create_table_if_not_exists here returns a new instance of DBTable. Alternatively, we could reflect a database table, in which we would not be required to provide a schema container.

''')

tab0 = None

@document.snippet
def create_table():
    global core, tab0
    with core.begin_ddl() as emitter:
        tab0 = emitter.create_table_if_not_exists(container_type=MyContainer0)
    for ci in core.inspect_columns('MyContainer0'):
        print(ci)

document.markdown('''

We can perform queries on the database using the ConnectQuery interface returned from the ConnectCore.query() method. In this case, we insert a new row into the database using the insert_multi() method. Not that we will use an alternative interface for inserting container instances into the database.

''')

@document.snippet
def query():
    global core, tab0
    with core.query() as q:
        q.insert_multi(tab0, [
            {'name': 'Devin J. Cornell', 'age': 50},
            {'name': 'Dorothy Andrews', 'age': 49},
        ])
        print(q.select(tab0.all_cols()).all())


document.markdown('''
To insert container object instances into the table, I instead use the DBTable.query() method to generate a TableQuery instance. This behaves much like ConnectQuery except that returned data will be placed into new container instances and we may insert data from container instances directly.
''')

@document.snippet
def query2():
    global tab0
    with tab0.query() as q:
        q.insert_single(MyContainer0(id=0, name='John Doe', age=30))
        print(q.select())

document.markdown('''
Here I define a more complicated schema.

+ The standard id column is now included. Notice that order=0 means the column will appear first in the table.
+ The updated and added attributes have been created to automatically record the time of insertion and update.
+ I added the birthyear method to the container type.

''')

MyContainer1 = None
import datetime

@document.snippet
def snippet():
    global MyContainer1
    
    import datetime
    @doctable.table_schema(table_name='mytable1')
    class MyContainer1:
        name: str
        age: int
        id: int = doctable.Column(
            column_args=doctable.ColumnArgs(order=0, primary_key=True, autoincrement=True),
        )
        updated: datetime.datetime = doctable.Column(
            column_args=doctable.ColumnArgs(default=datetime.datetime.utcnow),
        )
        added: datetime.datetime = doctable.Column(
            column_args=doctable.ColumnArgs(
                default=datetime.datetime.utcnow, 
                onupdate=datetime.datetime.utcnow,
            )
        )
        
        def birthyear(self):
            '''Retrieve the birthyear of the person at the time this database entry was added.'''
            try:
                return self.added.year - self.age
            except AttributeError as e:
                raise AttributeError('Cannot calculate birthyear without the added date. '
                    'Did you mean to call this on a retrieved container instance?') from e
        
    print(doctable.inspect_schema(MyContainer1).column_info_df())

document.markdown(
'''
We create this table just as we did the one before, and show the new schema using inspection.
'''
)

tab1 = 0
@document.snippet
def oof():
    global core, tab1
    with core.begin_ddl() as emitter:
        tab1 = emitter.create_table_if_not_exists(container_type=MyContainer1)

    for ci in core.inspect_columns('mytable1'):
        print(ci)


if __name__ == '__main__':

    print(document.render_html())


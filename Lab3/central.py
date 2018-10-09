class book:
    author=""
    title=""
    publication_year=0
    identifier=0

    def __init__(self,author,title,publication_year,identifier):
        self.author=author
        self.title=title
        self.publication_year=publication_year
        self.identifier=identifier

    def __repr__(self):
        return " ".join([ self.author,self.title,str(self.publication_year),str(self.identifier)])

class bookDB:
    array=[]

    def insert_book(self,books):
        for book in books:
            self.array.append(book)

    def show_book(self,book_identifier):
        for book in self.array:
            if book.identifier == book_identifier:
                print(book.__repr__())

    def list_all_authors(self):
        for book in self.array:
            print(book.author)

    def books_from_author(self,author):
        for book in self.array:
            if book.author == author:
                print(book.__repr__())

    def books_from_year(self,year):
        for book in self.array:
            if book.publication_year == year:
                print(book.__repr__())



book1=book("mondovil", "pissa : the birth of something", 2013, 696969)
book2=book("mondovil", "pissa2 : cums back", 2015, 696970)
book3 = book("mondovil", "pissa3 : the art of threesome", 2017, 696971)
book4 = book("tomacho", "ganza shark : belgian diplomat", 2016, 696972)
db=bookDB
db.insert_book(db,[book1,book2,book3,book4])
#db.books_from_author(db,"mondovil")
#db.books_from_year(db,2017)
db.list_all_authors(db)



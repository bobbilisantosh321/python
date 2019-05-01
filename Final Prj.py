#Pardhu Gorripati
#sqlalchemy components
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, not_

Base =  declarative_base()

class baseRoom(Base):
    #Database Table name
    __tablename__ = 'room'
    #Table Columns
    Id = Column(Integer, primary_key=True)
    Type = Column(String)
    __Price = Column(Float, primary_key=True)
    Status = Column(String)
    
    def __init__(self, Id, Type, Price):
        self.Id = Id
        self.Type = Type
        self.__Price = Price
        self.Status = 'A' #Default Room Status 'A' - Available
    
    def getPrice(self):
        return self.__Price

class personalProfile(Base):
    #Database Table name
    __tablename__ = 'person'
    #Table Columns
    Id = Column(Integer, primary_key=True)
    FName = Column(String)
    LName = Column(String)
    Type = Column(String)
    phone = Column(Integer)
    overdue = Column(String)
    
    def __init__(self, Id, FName, LName, Type, Phone):
        self.Id = Id
        self.FName = FName
        self.LName = LName
        self.Type = Type
        self.phone = Phone
        self.overdue = ''
    
    def getName(self):
        #Method to return User Name
        return str(self.FName) + ' ' + str(self.LName)

class baseReservation(Base):
    #Database Table name
    __tablename__ = 'reservations'
    #Table Columns
    RoomId = Column(Integer, primary_key=True)
    PersonId = Column(Integer, primary_key=True)
    FromDate = Column(Integer, primary_key=True)
    ToDate = Column(Integer)
    Status = Column(String)
    Charge = Column(Float)
    paymentStatus = Column(String)
    
    def __init__(self, RoomId, PersonId, FromDate, ToDate, Charge):
        self.RoomId = RoomId
        self.PersonId = PersonId
        self.FromDate = FromDate
        self.ToDate = ToDate
        self.Status = 'Booked' #Default Initial Status Booked
        self.Charge = Charge
        self.paymentStatus = '' #Default Payment Status Blank
    
    def getPersonInReservation(self):
        return self.PersonId
    
class manageDB():
    def __init__(self, databaseSession):
        self.dbSession = databaseSession

class managePerson(manageDB):
    def addPerson(self, Id, FName, LName, Type, Phone):
        person = personalProfile(Id, FName, LName, Type, Phone)
        self.dbSession.add(person)
        self.dbSession.commit()
        
        self.printPersonDetails(person)
    
    def printPersonDetails(self, person):
        print(person.getName(), "with ID", person.Id)
    
    def searchById(self, Id):
        person = self.dbSession.query(personalProfile).filter_by(Id = Id).first()
        
        if person != None:
            return person            
        
class manageRoom(manageDB):
    def addRoom(self, Id, Type, Price):
        
        room = baseRoom( Id, Type, Price)
        
        self.dbSession.add(room)
         
        self.dbSession.commit()
        
        self.printRoomDetails(room, True)
    
    def printRoomDetails(self, room, DbConfirmation=None):
        if DbConfirmation == True:
            print("Room", room.Id, "Type", room.Type, "with price $", room.getPrice(), "added to Database")
        else:
            print("Room", room.Id, "Type", room.Type, "with price $", room.getPrice())
    
    def checkDuplicateId(self, Id):
        
        room = self.searchRoomById(Id)

        if room != None:
            return True
        else:
            return False
        
    def searchRoomById(self, Id):
        room = self.dbSession.query(baseRoom).filter_by(Id = Id).first()
        
        if room != None:
            return room  
    
    def checkAvailablity(self, Type=None):

        if Type != None:
            rooms = self.dbSession.query(baseRoom).filter_by(Type = Type, Status = 'A').all()
        else:
            rooms = self.dbSession.query(baseRoom).filter_by(Status = 'A').all()
        
        for room in rooms:
            self.printRoomDetails(room)
            
class manageReservation(manageDB):
    def addReservation(self, RoomId, PersonId, FromDate, ToDate, RoomCharge):
        
        reservationToAdd = baseReservation(RoomId, PersonId, FromDate, ToDate, RoomCharge)
        
        self.dbSession.add(reservationToAdd)
         
        self.dbSession.commit()
        
        self.printReservationDetails(reservationToAdd, True)
    
    def searchReservation(self, RoomId, PersonId, FromDate):
        return self.dbSession.query(baseReservation).\
            filter_by(RoomId=RoomId, PersonId = PersonId, FromDate=FromDate).first()
    
    def printReservationDetails(self, reservation, DbConfirmation=None):
        
        rooms = manageRoom( self.dbSession )
        room = rooms.searchRoomById( reservation.RoomId )
        if room == None:
            print("No Room found for Room ID", reservation.RoomId)
        persons = managePerson( self.dbSession )
        personId = reservation.getPersonInReservation()
        person = persons.searchById( personId )
        if person == None:
            print("No Person found with ID", personId)
        
        if DbConfirmation == True:
            print("Room", reservation.RoomId, "Type", room.Type, "with status", reservation.Status, "& price $", reservation.Charge, "for", person.getName() , "added to Database")
        else:
            print("Room", reservation.RoomId, "Type", room.Type, "with status", reservation.Status, "& price $", room.getPrice())
    
    def cancelReservation(self, roomId, personId, FromDate):
         reservation = self.searchReservation( roomId, personId, FromDate )
         reservation.Status = "Cancelled"
         self.dbSession.commit()
        
class databaseSession(object):
    #Private variables to have instance & list
    __instance = None
    session = None
    
    def __new__(self):
        #New object contructor to always have one instance of Class
        #Check if there is already instance
        if databaseSession.__instance is None:
            #If no instance create one & save it to private variable
            databaseSession.__instance = object.__new__(self)
        #Return the instance saved in variable
        return databaseSession.__instance
    
    def createSession(self):
        
        if self.session == None:
            #Initiate DB connection to memory
            engine = create_engine('sqlite:///:memory:', echo=False)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            #Capture connection Session
            self.session = Session()
        
        return self.session

class GetInputAndValidate():
    def inputAny(self, inputText):
        return input(inputText)
    
    def inputText(self, inputText, errorText=None):
        
        while True:
            try:
                inputValue = str(input(inputText))
            except ValueError:
                self.errorMessage(errorText, "for text" )
            else:
                break
        return inputValue
            
        
    def validateNumberInput(self, inputText, errorText=None  ):
        #Function for valid number input
        while True:
            try:
                inputValue = int(input(inputText))
            except ValueError:
                self.errorMessage(errorText, "for number" )
            else:
                break
        return inputValue
    
    def validateFloatInput(self, inputText, errorText=None  ):
        #Function for valid number input
        while True:
            try:
                inputValue = float(input(inputText))
            except ValueError:
                self.errorMessage(errorText, "for number with decimals" )
            else:
                break
        return inputValue
    
    def invalidEntry(self, text ):
        #Function to print message for invalid input
        print("Invalid " + text +", please try again")
        print()
    
    def errorMessage(self,errorText, defaultText ):
        if errorText !=None:
            self.invalidEntry(errorText)
        else:
            self.invalidEntry(defaultText)

class inputRoomDetails(GetInputAndValidate):
    def __init__(self):
        self.roomType = ["Queen","King","Twin"]
    
    def checkRoomType(self, roomType):
        
        for type in self.roomType:
            if type.lower() == roomType.lower():
                return type
        
    def getRoomNumber(self, Add=None):
        
        if Add != None:
            dbConnection = databaseSession()
            roomCollection = manageRoom( dbConnection.session )
            while True:
                Id = self.validateNumberInput("Please Enter Room Number: ")
                if roomCollection.checkDuplicateId( Id ):
                    print("Room number already Used, please enter a unique Room number")
                else:
                    return Id                    
        else:
            return self.validateNumberInput("Please Enter Room Number: ")
    
    def getRoomPrice(self):
        
        return self.validateFloatInput("Please Enter Price for the Room: $", "for price")
    
    def getRoomType(self):
       
        while True:
            self.printRoomTypes()
            roomType = self.inputText("Please Enter valid Room Type: ", "Room type")
            roomType = self.checkRoomType( roomType )
            if roomType != None:
                return roomType
            else:
                self.errorMessage(None, "Room Type" )

    def printRoomTypes(self):
        print("\nSelect Room Type from below:")
        for type in self.roomType:
            print(type)
        
    def getInputRoomDetails(self, add=None):
        return self.getRoomNumber(add), self.getRoomType(), self.getRoomPrice()

class inputReservationDetails(GetInputAndValidate):
    def __init__(self):
        self.roomType = ["Queen","King","Twin"]

def main():
    dbConnection = databaseSession()
    dbConnection.createSession()
    
    roomDetails = inputRoomDetails( )
    roomCollection = manageRoom( dbConnection.session )
    roomCollection.addRoom(1, 'Queen', 12)
    
    roomId, roomType, roomPrice = roomDetails.getInputRoomDetails(True)
    
    roomCollection.addRoom(roomId, roomType, roomPrice)
    
    print()
    print("Show all availability")
    roomCollection.checkAvailablity()
    print()
    print("Show only Queen availability")
    roomCollection.checkAvailablity("Queen")
    
    profiles = managePerson(  dbConnection.session )
    profiles.addPerson(1, 'David', 'Thonny', 'C', 9521231234)
    print("Person added to DB")
    print()
    print("Searching person with ID 1")
    dbPerson = profiles.searchById(1)
    profiles.printPersonDetails(dbPerson)
    
    mngReservations = manageReservation( dbConnection.session )
    
    mngReservations.addReservation( 1, 1, 20190806, 20190808, 20.1)
    
    mngReservations.cancelReservation(1, 1, 20190806)
    
    mngReservations.printReservationDetails(mngReservations.searchReservation(1, 1, 20190806))

main()
    

from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///thislab.db')
Session = sessionmaker(bind=engine)
session =Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer(), primary_key=True)
    actor = Column(String()) 
    location = Column(String()) 
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer(), ForeignKey('roles.id')) 
    roles = relationship('Role', back_populates = 'audition')

    def call_back(self):
        self.hired = True
        session.commit()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String()) 
    audition = relationship('Audition', back_populates = 'roles')

    def auditions(self):
        audition_list = []
        for audtion in session.query(Audition).all():
            if audtion.role_id == self.id:
                audition_list.append(audtion)
        print(len(audition_list), 'this is the auditon list')
        return audition_list
    
    def actors(self):
        actor_list = []
        for audtion in session.query(Audition).all():
            if audtion.role_id == self.id:
                actor_list.append(audtion.actor)
        print(actor_list)
        return actor_list
    
    def locations(self):
        location_list = []
        for audtion in session.query(Audition).all():
            if audtion.role_id == self.id:
                location_list.append(audtion.location)
        print(location_list)
        return location_list
    
   
    def lead(self):
        for audtion in session.query(Audition).all():
            if audtion.role_id == self.id and audtion.hired == True:
                print(audtion.actor)
                return audtion
        else:
                 print('No actor has been hired for understudy for this role')
            
    def understudy(self):
        return_list = []
        for audtion in session.query(Audition).all():
            if audtion.role_id == self.id and audtion.hired == True:
                return_list.append(audtion)
        if len(return_list) >= 2:
            print(return_list[1].actor)
            return return_list[1]
        else:
            print('No actor has been hired for understudy for this role')




# ============TESTING==================

session.query(Role).delete()
session.query(Audition).delete()

r1 = Role(character_name = 'Michael')
r2 = Role(character_name = 'John')

session.add(r1)
session.commit()
session.add(r2)
session.commit()
a1 = Audition(actor='peter', location='florida', phone=5555555555, hired= True, role_id = r1.id)
a2 = Audition(actor='paul', location='new york', phone=5555555555, hired= False, role_id = r1.id)
a3 = Audition(actor='mark', location='california', phone=5555555555, hired= False, role_id = r1.id)

session.add_all([a1, a2, a3])
session.commit()



# print('this shit is working?', a1.roles)
# print('this id should match', r1)
# print(a1.call_back())
r1.lead()
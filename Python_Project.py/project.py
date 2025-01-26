# list ที่เก็บ dict รหัส ชื่อ สกุล =======================================================
import csv 
import datetime
import time
listid,listfname,listlname,std_dict=[],[],[],{}
Lecture,Lab=['IT301', 'IT302', 'IT303', 'IT304'],['LAB103', 'LAB104', 'LAB105', 'LAB106']

with open ('students.csv') as file: #คำสั่ง open เปิดไฟล์ demo.csv เก็บไว้ที่ตัวแปร file และ with เป็น statement ที่ช่วยสร้าง context manager มันจะช่วยปิดไฟล์ให้เราทันทีที่เราใช้งานเสร็จแล้ว (ไม่งั้นจะต้องเรียก method ที่ชื่อว่า close() อีกตัวหนึ่งเพื่อปิดไฟล์เอง)
    csvreader = csv.reader(file) #อ่านข้อมูลจากตัวแปร file เก็บไว้ที่ตัวแปร csvreader
    for col in csvreader: 
        listid.append(col[0])
        listfname.append(col[1])
        listlname.append(col[2])
        std_dict[col[0]] = (col[1:])

data = [
    ["ID", "Room Type", "Room Number", "Date"],
    ["S001", "Lecture", "IT301", "01-12-2024"],
    ["S002", "Lab", "LAB103", "02-12-2024"],
    ["S003", "Lecture", "IT302", "03-12-2024"],
    ["S004", "Lab", "LAB104", "04-12-2024"],
]

# สร้างไฟล์ Book1.csv
with open("Book1.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)


def openid():
    with open('Book1.csv','r',encoding='utf-8-sig') as csv_file: # r อ่าน file 
        csv_reader = csv.reader(csv_file) #เก็บที่ csv_file
        return list(csv_reader) #return ค่าไปที่ openid()

def date(dc):
    try:
        datetime.datetime.strptime(dc,'%d-%m-%Y') #เปลี่ยน str เป็น date
        return True 
    except ValueError:
        return False

# [ 1 ] print a list of students ===================================================
def studentname ():
    print("ID         NAME         LASTNAME")
    for i in range (1,len(listid)): #loop ตามจำนวนค่าที่อยู่ใน listid
        print (f"{listid[i]}    {listfname[i]} \t{listlname[i]}") #print first line ตามจำนวน i

# [ 2 ] booking request =============================================================
def booking():
    def check_duplicate_booking(roomnumber,dc): #function 
        for row in openid():  #row คือแต่ละบรรทัดในไฟล์ openid
                if row[2] == roomnumber.upper() and row[3] == dc.upper():  #print indexที่2และ3
                    return True #ถ้าเงือนไขเป็นจริง return True
        return False     #if condition not true, return false
    id = input("ID : ") #รับรหัสนักศึกษา
    if id in listid: #ถ้ารหัสนักศึกษาตรง
        room_type=input("Room types (Lecture/Lab): ") #รับค่า

        if room_type.lower() =='lecture': #ถ้า input คือ Lecture
            print(Lecture) #print list Lecture 
            while True: #ลูปเพื่อให้กรอกข้อมูลจนกว่าจะถูก
                roomnumber=input('Please select one room above: ') #input
                if roomnumber.upper() in Lecture: #ถ้าห้องที่เลือก อยู่ใน list lecture จริง
                    dc=input("Booking date (DD-MM-YYYY): ") #ระบุเวลา
                    if date(dc):
                        break
                    else:
                        return('Incorrect date format, should be DD-MM-YYYY ')
                else:
                    print ('Error plaese try again')

        elif room_type.lower()=='lab':
            print(Lab)
            while True:
                roomnumber=input('Please select one room above: ')
                if roomnumber.upper() in Lab:
                    dc=input("Booking date (DD-MM-YYYY): ")
                    if date(dc):
                        break
                    else:
                        return('Incorrect date format, should be DD-MM-YYYY ')
                else:
                    print ('Error plaese try again')
        else:
            return ('Error Room Type plaese try again')
    else:
        return('Student Not Found')

    bookingData=[id,room_type.lower(),roomnumber.upper(),dc]
    if check_duplicate_booking(roomnumber, dc): #ประกาศใช้ฟังชั่น ถ้า return True ให้ทำเงือนไข
        return(f"Room number {roomnumber} is already booked on {dc}.")
    else:
        with open('Book1.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file) #เขียนข้อมูลลงไฟล์ csv
            csv_writer.writerow(bookingData)
        return(f"Booking for room number {roomnumber} on {dc} is successful.")
    
# [ 3 ] check the current booking by room number ==================================
def checkbyroomnumber():
    while True:
        check=input("Room number: ")
        if check.upper() in Lecture or check.upper() in Lab:
            break
        else:
            print ('please enter room number again\n\n')
    print ('Current booking: ')
    count=0
    for row in openid():  
        if row[2]==check.upper():
            print(f'  Date : {row[3]} Student {row[0]}')
            count+=1
    if count==0:
        print ('No booking')

# [ 4 ] check the available rooms via date =========================================
def date_check():
    book=[]
    def duplicate(dc):
        lec=Lecture.copy()
        la=Lab.copy()
        for row in openid():  #แต่ละแถวใน csv_file ที่เป็น list
            if dc == row[3]:
                book.append(row[2])
                for item in book:
                    if item in lec:
                        lec.remove(item)
                    if item in la:
                        la.remove(item)
        print (f'Lecture : {lec} \n Lab : {la}')
        
    while True:
        dc=input('Checking date (DD-MM-YYYY): ')
        if date(dc):
            print ('Available rooms: ')
            duplicate(dc)
            break
        else:
            print ('Incorrect date format, should be DD-MM-YYYY ')

# [ 5 ] check booking with student ID ==============================================
def check_id():
    Id=input('ID: ')
    if Id in listid:       
        print ('Current bookings: ')
        count=0
        for row in openid():  #แต่ละแถวใน csv_file ที่เป็น list
            if Id==row[0]:
                print (f'Room: {row[2]} Date: {row[3]}' )
                count+=1
        if count==0:
            print ('No booking')
    else:
        print ('Student Not Found')

# [ 6 ] check booking with student first name =======================================
idcheck=[]
def check_name():
    matching=[]
    inputname = input('input name : ')
    a=0
    for name in listfname:
        if inputname.lower() in name.lower():
            matching.append(name)
            a=1
    if a==0:
        print ('there is no student found ')
    if matching:
        for nm in matching:
            for k,v in std_dict.items():
                if nm==v[0]:
                    print (k,v[0],v[1])
                    count=0
                    for row in openid():
                        if row[0]==k :
                            print (f'Room number {row[2]} is already booked on {row[3]}')
                            count+=1
                    if count==0:
                        print ('no booking')

# [ 7 ] print booking summary ======================================================***when you use function 4 
def booking_summary():
    print ('Lecture')
    for i in Lecture:
        print (i)
        A=0
        for j in openid():
            if i==j[2]:
                print (f'  Date : {j[3]} Student {j[0]}')
                A=1
        if A==0:
            print ('No Booking')
    print ('\nLab')
    for i in Lab:
        print (i)
        A=0
        for j in openid():
            if i==j[2]:
                print (f'  Date : {j[3]} Student {j[0]}')
                A=1
        if A==0:
            print ('No Booking')                                
# ลูปหลัก ให้userเลือก ================================================================
while True:
    print ('\n\ndelay 1 sec\n\n'), time.sleep(1)
    print ('''\n\nMUICT Student Room Booking System\n 1. print a list of students \n 2. submit a booking request\n 3. check the current booking via room number\n 4. check the available rooms via date\n 5. check booking with student ID \n 6. check booking with student first name \n 7. print booking summary \n  0. exit ''')
    n=int(input("Option:"))
    print (" \n\n")
    actions = {
        1: studentname,
        2: lambda: print(booking()),
        3: checkbyroomnumber,
        4: date_check,
        5: check_id,
        6: check_name,
        7: booking_summary,
        0: lambda: print('Thank you') or exit(),}
    action = actions.get(n ,lambda : print('try again')) #จะเก็บ value ซึง value คือ ชื่อของ function \\ lambda คือ ค่า default paramrter 
    action() # () ไว้เรียกใช้ func ที่เก็บใน action

#ตัดส่วนที่ไม่จำเป็น ทำให้โค้ดสั้นลง
#ส่วนไหนสามารถใช้ lambda ได้ เปลี่ยนเป็น lamda 




#include <Wire.h> 
#include <JY901.h>
#include <Servo.h>  
/*#include <SoftwareSerial.h>    //使用软件串口，能讲数字口模拟成串口
SoftwareSerial mySerial(2, 3);    //软串口的Rx、Tx 对应于板子上的 D2 D3
*/

Servo rudder;    //初始化船舵        
Servo sail;    //初始化船帆
int pos1 = 89;    //船舵-舵机角度
int pos2 = 73;    //船帆-舵机角度

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
  /*mySerial.begin(9600);*/
  Serial.begin(9600);    //设置蓝牙传输速率
  Serial.println("Yep,I am the SoftwareSerail!");  // 检测蓝牙连接
    
  rudder.attach(9);     //将船舵与pin9连接
  sail.attach(10);     //将船帆与pin10连接
  
  JY901.StartIIC();     //IMU启动IIC通讯
  while(Serial.read()>=0){}; // 清空serialBuffer
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  
    //   Boat Control   //  
   if (Serial.available()) {      //蓝牙收到消息    
     char command = Serial.read();
     if(command =='d')                    //右打舵
      {   
          pos1=pos1-6;
          if(pos1<55) pos1=55;             // 舵电机不可小于55°
          rudder.write(pos1);
          // Serial.println('HEYHEY');
      }
      else if(command =='a')              //左打舵
      {  
          pos1=pos1+6;
          if (pos1>115) pos1=115;         // 舵电机不可超过115°
          rudder.write(pos1);                     
      }
      else if (command =='s')            //舵回正
      {
          pos1=89;
          rudder.write(pos1);
      }
      else if(command =='o')             //紧帆
      {  
          pos2=95; 
          sail.write(pos2);  
          // Serial.println("jinfan");                
      }
      else if(command =='k')             //松帆
      {  
          pos2=51;
          sail.write(pos2);
          // Serial.println("songfan");                    
                  
      } 
   
    //     IMU section     //       
    JY901.GetAngle();   //获取角度信息
    Serial.println((float)JY901.stcAngle.Angle[2]/32768*180);
    delay(200);
  }
    // JY901.GetAngle();   //获取角度信息
    // Serial.println((float)JY901.stcAngle.Angle[2]/32768*180);
    // delay(200);
}

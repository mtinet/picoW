from machine import I2C, Pin
import time

# MPU6050 장치 주소 및 레지스터 주소
MPU6050_ADDR = 0x68
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48
PWR_MGMT_1 = 0x6B

# I2C 객체 초기화
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# MPU6050을 깨우기 위한 함수
def wake_mpu6050():
    i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, bytearray([0x00]))

# 센서 데이터를 읽는 함수
def read_mpu6050():
    # 가속도 센서 데이터 읽기
    accel_x = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_XOUT_H, 2)
    accel_y = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_H, 2)
    accel_z = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_ZOUT_H, 2)

    # 온도 데이터 읽기
    temp = i2c.readfrom_mem(MPU6050_ADDR, TEMP_OUT_H, 2)

    # 자이로스코프 데이터 읽기
    gyro_x = i2c.readfrom_mem(MPU6050_ADDR, GYRO_XOUT_H, 2)
    gyro_y = i2c.readfrom_mem(MPU6050_ADDR, GYRO_YOUT_H, 2)
    gyro_z = i2c.readfrom_mem(MPU6050_ADDR, GYRO_ZOUT_H, 2)

    # 16비트 2진수 데이터를 실제 값으로 변환
    accel_x = int.from_bytes(accel_x, 'big') if accel_x[0] < 0x80 else int.from_bytes(accel_x, 'big') - 65536
    accel_y = int.from_bytes(accel_y, 'big') if accel_y[0] < 0x80 else int.from_bytes(accel_y, 'big') - 65536
    accel_z = int.from_bytes(accel_z, 'big') if accel_z[0] < 0x80 else int.from_bytes(accel_z, 'big') - 65536
    temp = int.from_bytes(temp, 'big') if temp[0] < 0x80 else int.from_bytes(temp, 'big') - 65536
    gyro_x = int.from_bytes(gyro_x, 'big') if gyro_x[0] < 0x80 else int.from_bytes(gyro_x, 'big') - 65536
    gyro_y = int.from_bytes(gyro_y, 'big') if gyro_y[0] < 0x80 else int.from_bytes(gyro_y, 'big') - 65536
    gyro_z = int.from_bytes(gyro_z, 'big') if gyro_z[0] < 0x80 else int.from_bytes(gyro_z, 'big') - 65536

    # 온도를 섭씨로 변환
    temp = (temp / 340.0) + 36.53

    return (accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z)

# MPU6050 깨우기
wake_mpu6050()

# 메인 루프
while True:
    # 센서 값 읽기
    accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z = read_mpu6050()

    # 센서 값 출력
    print('Acceleration X: {}, Y: {}, Z: {}'.format(accel_x, accel_y, accel_z), '   Gyroscope X: {}, Y: {}, Z: {}'.format(gyro_x, gyro_y, gyro_z), '   Temperature: {} C'.format(temp))

    # 1초 대기
    time.sleep(0.1)

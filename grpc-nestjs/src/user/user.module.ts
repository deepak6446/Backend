import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { join } from 'path';
import { UserController } from './user.controller';

const port = process.env.PORT || '5000';

@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'USER_PACKAGE',
        transport: Transport.GRPC,
        options: {
          url: 'localhost:' + port,
          package: 'user',
          protoPath: join(__dirname, 'user.proto'),
        },
      },
    ]),
  ],
  controllers: [UserController],
})
export class UserModule {}

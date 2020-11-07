import { NestFactory } from '@nestjs/core';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { join } from 'path';
import { AppModule } from './app.module';

/**
 * This file contains code for rest API and grpc server
 * Rest API is used to test grpc server
 */

async function bootstrap() {
  console.log(`******* ENVIRONMENT: ${process.env.ENVIRONMENT} ******* `);

  //grpc server
  if (process.env.ENVIRONMENT == 'server') {
    const port = process.env.PORT || '5000';
    const app = await NestFactory.createMicroservice<MicroserviceOptions>(
      AppModule,
      {
        transport: Transport.GRPC,
        options: {
          url: 'localhost:' + port,
          package: 'user',
          protoPath: join(__dirname, 'user/user.proto'),
        },
      },
    );
    console.log(`listening on port: ${port}`);
    await app.listenAsync();
  } else {
    //client to test grpc API
    const app = await NestFactory.create(AppModule);
    app.connectMicroservice<MicroserviceOptions>({
      transport: Transport.GRPC,
      options: {
        package: 'user',
        protoPath: join(__dirname, './user/user.proto'),
      },
    });

    await app.startAllMicroservicesAsync();
    await app.listen(3001);
    console.log(`Application is running on: ${await app.getUrl()}`);
  }
}
bootstrap();

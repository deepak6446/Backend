import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { MongooseModule } from '@nestjs/mongoose';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ItemsModule } from './items/items.module';

@Module({
  imports: [
    ItemsModule,
    MongooseModule.forRoot('mongodb://localhost:27017/nestgraphql'),
    GraphQLModule.forRoot({
      autoSchemaFile: 'schema.gql', //auto generated GraphQL file that get’s created when we start the server.
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

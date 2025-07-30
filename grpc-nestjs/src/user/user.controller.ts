import { Controller, Get, Inject, Param } from '@nestjs/common';
import { ClientGrpc, GrpcMethod } from '@nestjs/microservices';
import { Observable } from 'rxjs';
import { UserById } from './interfaces/user-by-id.interface';
import { User } from './interfaces/user.interface';

interface UserService {
  findOne(data: UserById): Observable<User>;
}

@Controller('user')
export class UserController {
  private userService: UserService;
  private readonly items: User[] = [
    { id: 1, name: 'John', email: 'john@gmail.com' },
    { id: 2, name: 'Doe', email: 'doe@gmail.com' },
  ];

  constructor(@Inject('USER_PACKAGE') private readonly client: ClientGrpc) {}

  onModuleInit() {
    this.userService = this.client.getService<UserService>('UserService');
  }

  @GrpcMethod('UserService')
  findOne(data: UserById): User {
    return this.items.find(({ id }) => id === data.id);
  }

  /**
   * Rest API to get data from grpc API
   * @param id unique item id
   */
  @Get(':id')
  getById(@Param('id') id: string): Observable<User> {
    return this.userService.findOne({ id: +id });
  }
}

import { InputType, Field, Int } from '@nestjs/graphql';

@InputType()
export class ItemInput {
  @Field(() => String)
  readonly title: string;
  @Field(() => Int)
  readonly price: number;
  @Field(() => String)
  readonly description: string;
}

import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as spotify_lambda from '../lib/spotify_lambda';

export class SpotifyLambdaStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new spotify_lambda.SpotifyLambda(this, "SpotifyLambda");
  }
}

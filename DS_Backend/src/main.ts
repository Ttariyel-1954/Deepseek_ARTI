import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module.js';
import { AllExceptionsFilter } from './common/filters/all-exceptions.filter.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api/v1');
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
      transformOptions: { enableImplicitConversion: false },
    }),
  );
  app.enableCors();
  app.useGlobalFilters(new AllExceptionsFilter());

  const cfg = new DocumentBuilder()
    .setTitle('Deepseek ARTI API')
    .setDescription('Azerbaycan Respublikasinin Tehsil Institutu — ERP backend')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, cfg));

  const port = process.env.PORT ?? 4000;
  await app.listen(port);
  console.log('API:       http://localhost:' + port + '/api/v1');
  console.log('Senedler:  http://localhost:' + port + '/docs');
}
bootstrap();

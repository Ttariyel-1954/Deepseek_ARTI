import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // 1) Butun endpoint-ler /api/v1 ile baslayir
  app.setGlobalPrefix('api/v1');

  // 2) DTO validasiyasi + tip cevrilmesi
  app.useGlobalPipes(
    new ValidationPipe({ whitelist: true, transform: true }),
  );

  // 3) Frontend (baska port) muraciet ede bilsin
  app.enableCors();

  // 4) Swagger
  const config = new DocumentBuilder()
    .setTitle('Deepseek ARTI API')
    .setDescription('Azerbaycan Respublikasinin Tehsil Institutu — ERP backend')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, config));

  const port = process.env.PORT ?? 4000;
  await app.listen(port);
  console.log('API hazirdir: http://localhost:' + port + '/api/v1');
  console.log('Senedler:    http://localhost:' + port + '/docs');
}

bootstrap();

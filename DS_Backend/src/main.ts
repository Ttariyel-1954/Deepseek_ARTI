import 'reflect-metadata';
import { Logger, ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module.js';
import { AllExceptionsFilter } from './common/filters/all-exceptions.filter.js';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);

  // Bütün endpoint-lər /api/v1 altında olsun
  app.setGlobalPrefix('api/v1');

  // Gələn məlumatı avtomatik yoxla və sinifə çevir
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,            // DTO-da olmayan sahələri sil
      forbidNonWhitelisted: true, // ...və ya şikayət et
      transform: true,            // "5" → 5 kimi çevirmələr
    }),
  );

  // Xətaları vahid formata sal
  app.useGlobalFilters(new AllExceptionsFilter());

  // Swagger sənədləşdirmə — /docs
  const konfiq = new DocumentBuilder()
    .setTitle('ARTİ ERP API')
    .setDescription('Azərbaycan Respublikasının Təhsil İnstitutu — ERP sistemi')
    .setVersion('0.1.0')
    .build();
  SwaggerModule.setup('docs', app, SwaggerModule.createDocument(app, konfiq));

  // CORS — frontend ayrı portda işləyəcək
  app.enableCors();

  const port = Number(process.env.PORT ?? 4000);
  await app.listen(port);

  Logger.log(`API hazırdır → http://localhost:${port}/api/v1`, 'BAŞLANGIC');
  Logger.log(`Sənədləşdirmə → http://localhost:${port}/docs`, 'BAŞLANGIC');
}

bootstrap();

import { Controller, Get, Header, Res } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import type { Response } from 'express';
import { IxracService } from './ixrac.service.js';
import { Roles } from '../auth/decorators/roles.decorator.js';

@ApiTags('ixrac')
@ApiBearerAuth()
@Controller('ixrac')
export class IxracController {
  constructor(private readonly ixrac: IxracService) {}

  @Get('emekdaslar.xlsx')
  @ApiOperation({ summary: 'Emekdaslari Excel-e cixar' })
  @Header('Content-Type',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  async emekdaslar(@Res() cavab: Response) {
    const bufer = await this.ixrac.emekdaslarExcel();
    cavab.setHeader('Content-Disposition',
      'attachment; filename="emekdaslar.xlsx"');
    cavab.send(bufer);
  }

  @Get('budce.xlsx')
  @ApiOperation({ summary: 'Budceni Excel-e cixar' })
  @Roles('admin', 'maliyyeci')
  @Header('Content-Type',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  async budce(@Res() cavab: Response) {
    const bufer = await this.ixrac.budceExcel();
    cavab.setHeader('Content-Disposition', 'attachment; filename="budce.xlsx"');
    cavab.send(bufer);
  }

  @Get('hesabat.html')
  @ApiOperation({
    summary: 'HTML hesabat — brauzerde Ctrl+P ile PDF kimi saxlanilir',
  })
  @Header('Content-Type', 'text/html; charset=utf-8')
  async hesabat(@Res() cavab: Response) {
    cavab.send(await this.ixrac.htmlHesabat());
  }
}

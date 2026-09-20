import {
  CanActivate, ExecutionContext, ForbiddenException, Injectable,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLLAR_ACARI } from '../decorators/roles.decorator.js';
import { Rol } from '../dto/qeydiyyat.dto.js';

/**
 * RBAC — Role-Based Access Control.
 * @Roles(...) ile isarelenmis endpoint-e yalniz hemin rollar gire biler.
 */
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const teleb = this.reflector.getAllAndOverride<Rol[]>(ROLLAR_ACARI, [
      context.getHandler(),
      context.getClass(),
    ]);

    // @Roles yoxdursa — her bir autentifikasiya olunmus istifadeci gire biler
    if (!teleb || teleb.length === 0) return true;

    const sorqu = context.switchToHttp().getRequest();
    const istifadeci = sorqu.user as { rol?: string } | undefined;

    if (!istifadeci?.rol) {
      throw new ForbiddenException('İstifadəçi rolu müəyyən deyil');
    }

    // 'admin' HER SEYE icazelidir — super-rol
    if (istifadeci.rol === 'admin') return true;

    if (!teleb.includes(istifadeci.rol as Rol)) {
      throw new ForbiddenException(
        `Bu əməliyyat üçün icazəniz yoxdur. ` +
        `Tələb olunan rol: ${teleb.join(' və ya ')}. Sizin rol: ${istifadeci.rol}`,
      );
    }

    return true;
  }
}

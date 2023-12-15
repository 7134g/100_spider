// Code generated by gen. DO NOT EDIT.

package query

import (
	"content_svr/app/maozhua_admin_svr/common/xerr"
	"content_svr/db/mysqldb/model"
	"context"
	"github.com/zeromicro/go-zero/core/logx"
	"gorm.io/gen"
	"gorm.io/gen/field"
)

func (p *{{.LowerType}}) ParseWhere(where map[string]interface{}) []gen.Condition {
	eqConds := make([]gen.Condition, 0)
	for key, v := range where {
		d := &fieldValue{value: v}
		eqConds = append(eqConds, field.NewField(p.TableName(), key).Eq(d))
	}

	return eqConds
}

func (p *{{.LowerType}}) Find(ctx context.Context, limit, offset int, where map[string]interface{}) ([]*model.{{.Type}}, error) {
	conds := p.ParseWhere(where)
	_db := p.WithContext(ctx)
	if limit != 0 {
		_db = _db.Limit(limit)
	}
	if offset != 0 {
		_db = _db.Offset(offset)
	}
	if where != nil {
		_db = _db.Where(conds...)
	}

	return _db.Find()
}

func (p *{{.LowerType}}) FindOne(ctx context.Context, where map[string]interface{}) (*model.{{.Type}}, error) {
	conds := p.ParseWhere(where)
	_db := p.WithContext(ctx)

	if where != nil {
		_db = _db.Where(conds...)
	}

	return _db.Take()
}

func (p *{{.LowerType}}) Update(ctx context.Context, where, update map[string]interface{}) (info gen.ResultInfo, err error) {
	conds := p.ParseWhere(where)
	if len(conds) == 0 {
		return gen.ResultInfo{}, xerr.DbUpdateMastWhere
	}
	info, err = p.WithContext(ctx).Where(conds...).Updates(update)
	if info.RowsAffected == 0 {
		logx.Infow("invalid update",
			logx.Field("table_name", p.TableName()),
			logx.Field("table_name_filter", where),
			logx.Field("table_name_data", update),
		)
	}
	return info, err
}
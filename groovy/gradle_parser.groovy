import com.thoughtworks.xstream.io.binary.Token
import org.codehaus.groovy.ast.ASTNode
import org.codehaus.groovy.ast.CodeVisitorSupport
import org.codehaus.groovy.ast.builder.AstBuilder
import org.codehaus.groovy.ast.expr.BinaryExpression
import org.codehaus.groovy.ast.expr.ClosureExpression
import org.codehaus.groovy.ast.expr.MethodCallExpression
import org.codehaus.groovy.ast.expr.ArgumentListExpression
import org.codehaus.groovy.ast.expr.ConstantExpression


/**
 *  Created by web on 2017/2/22.
 */




class WarBlockVisitor extends CodeVisitorSupport{
    public String baseName

    @Override
    void visitBinaryExpression(BinaryExpression expression) {
        if (expression.leftExpression.variable == "baseName") {
            baseName = expression.rightExpression.value
        }
    }
}


class TaskBlockVisitor extends CodeVisitorSupport {
    @Override
    void visitConstantExpression(ConstantExpression expression) {
        if(expression.leftExpression.variable == "project.disconf.df_host") {
            if(expression.rightExpression.value != "disconfig.nxin.com")
                throw Exception("域名配置错误")
        }
    }
}

class GradleVisitor extends CodeVisitorSupport  {
    public String version
    public WarBlockVisitor warBlock

    static setBlockVisitor(ArgumentListExpression ale, CodeVisitorSupport visitor) {
        if (ale.size() == 1 && ale[0] instanceof ClosureExpression) {
            ale[0].getCode().visit(visitor)
        } else {
            throw IndexOutOfBoundsException("ArgumentListExpression size is not 1")
        }
    }

    @Override
    void visitBinaryExpression(BinaryExpression expression) {
        // foo = bar
        if (expression.leftExpression.variable == "version") {
            version = expression.rightExpression.value // ConstantExpression
        }
    }

    @Override
    void visitMethodCallExpression(MethodCallExpression call) {
        ArgumentListExpression ale
        // method {}
        if (call.getMethodAsString() == "war") {
            ale = call.getArguments() as ArgumentListExpression
            warBlock = new WarBlockVisitor()
            setBlockVisitor(ale, warBlock)
        } else
        // task name {}
        if (call.getMethodAsString() == "task") {
            ale = call.getArguments() as ArgumentListExpression
            if (ale.size() == 1 && ale[0] instanceof MethodCallExpression) {
                if (ale[0].getMethodAsString() == "prod") {
                    println("find prod")
                }
            }
        }
    }
}

AstBuilder builder = new AstBuilder()
nodes = builder.buildFromString(new File("build.gradle").text)
gradle = new GradleVisitor()
for (ASTNode node : nodes) {
    node.visit(gradle)
}
println("version: $gradle.version")
println("baseName $gradle.warBlock.baseName")
